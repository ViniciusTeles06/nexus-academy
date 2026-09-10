const API_URL = (
  process.env.NEXT_PUBLIC_API_URL ?? ""
).replace(/\/$/, "");

const ACCESS_TOKEN_KEY = "nexus_access";
const USER_KEY = "nexus_user";

const ACTIVE_INSTITUTION_KEY =
  "nexus_active_institution";

const ACTIVE_MEMBERSHIP_KEY =
  "nexus_active_membership";


export type Institution = {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
};


export type MembershipRole =
  | "OWNER"
  | "ADMIN"
  | "TEACHER"
  | "STUDENT";


export type MembershipStatus =
  | "INVITED"
  | "ACTIVE"
  | "SUSPENDED"
  | "INACTIVE";


export type Membership = {
  id: string;

  institution: Institution;

  role: MembershipRole;

  status: MembershipStatus;

  created_at: string;
};


function getSessionStorage() {
  if (typeof window === "undefined") {
    return null;
  }

  return window.sessionStorage;
}


function buildApiUrl(
  endpoint: string,
) {
  if (
    endpoint.startsWith("http://") ||
    endpoint.startsWith("https://")
  ) {
    return endpoint;
  }

  if (!API_URL) {
    throw new Error(
      "NEXT_PUBLIC_API_URL não foi configurada.",
    );
  }

  const normalizedEndpoint =
    endpoint.startsWith("/")
      ? endpoint
      : `/${endpoint}`;

  return `${API_URL}${normalizedEndpoint}`;
}


/* ========================================
   ACCESS TOKEN
======================================== */

export function getAccessToken() {
  return (
    getSessionStorage()?.getItem(
      ACCESS_TOKEN_KEY,
    ) ?? null
  );
}


export function saveAccessToken(
  token: string,
) {
  getSessionStorage()?.setItem(
    ACCESS_TOKEN_KEY,
    token,
  );
}


/* ========================================
   USER
======================================== */

export function saveUser(
  user: unknown,
) {
  getSessionStorage()?.setItem(
    USER_KEY,
    JSON.stringify(user),
  );
}


export function getSavedUser<T = unknown>() {
  const value =
    getSessionStorage()?.getItem(
      USER_KEY,
    );

  if (!value) {
    return null;
  }

  try {
    return JSON.parse(
      value,
    ) as T;
  } catch {
    return null;
  }
}


/* ========================================
   ACTIVE INSTITUTION
======================================== */

export function getActiveInstitutionId() {
  return (
    getSessionStorage()?.getItem(
      ACTIVE_INSTITUTION_KEY,
    ) ?? null
  );
}


export function getActiveMembership() {
  const value =
    getSessionStorage()?.getItem(
      ACTIVE_MEMBERSHIP_KEY,
    );

  if (!value) {
    return null;
  }

  try {
    return JSON.parse(
      value,
    ) as Membership;
  } catch {
    return null;
  }
}


export function saveActiveMembership(
  membership: Membership,
) {
  const storage =
    getSessionStorage();

  if (!storage) {
    return;
  }

  storage.setItem(
    ACTIVE_INSTITUTION_KEY,
    membership.institution.id,
  );

  storage.setItem(
    ACTIVE_MEMBERSHIP_KEY,
    JSON.stringify(
      membership,
    ),
  );
}


export function clearActiveMembership() {
  const storage =
    getSessionStorage();

  if (!storage) {
    return;
  }

  storage.removeItem(
    ACTIVE_INSTITUTION_KEY,
  );

  storage.removeItem(
    ACTIVE_MEMBERSHIP_KEY,
  );
}


/* ========================================
   SESSION
======================================== */

export function clearSession() {
  const storage =
    getSessionStorage();

  if (!storage) {
    return;
  }

  storage.removeItem(
    ACCESS_TOKEN_KEY,
  );

  storage.removeItem(
    USER_KEY,
  );

  storage.removeItem(
    ACTIVE_INSTITUTION_KEY,
  );

  storage.removeItem(
    ACTIVE_MEMBERSHIP_KEY,
  );
}


/* ========================================
   REFRESH TOKEN
======================================== */

let refreshPromise:
  Promise<string | null> | null =
  null;


async function performRefresh() {
  try {
    const response =
      await fetch(
        buildApiUrl(
          "/api/v1/auth/refresh/",
        ),
        {
          method: "POST",

          credentials:
            "include",
        },
      );

    if (!response.ok) {
      clearSession();

      return null;
    }

    const data =
      (await response.json()) as {
        access?: string;
      };

    if (!data.access) {
      clearSession();

      return null;
    }

    saveAccessToken(
      data.access,
    );

    return data.access;
  } catch {
    clearSession();

    return null;
  }
}


export function refreshAccessToken() {
  /*
    Impede várias chamadas simultâneas
    ao refresh token.

    Isso será importante quando o
    dashboard carregar notas,
    frequência, disciplinas etc.
    ao mesmo tempo.
  */

  if (refreshPromise) {
    return refreshPromise;
  }

  refreshPromise =
    performRefresh().finally(
      () => {
        refreshPromise = null;
      },
    );

  return refreshPromise;
}


/* ========================================
   BASE REQUEST
======================================== */

async function request(
  endpoint: string,
  accessToken:
    | string
    | null,
  options: RequestInit = {},
) {
  const headers =
    new Headers(
      options.headers,
    );

  /*
    JWT
  */

  if (accessToken) {
    headers.set(
      "Authorization",
      `Bearer ${accessToken}`,
    );
  }

  /*
    Instituição atualmente
    selecionada.
  */

  const institutionId =
    getActiveInstitutionId();

  if (institutionId) {
    headers.set(
      "X-Institution-ID",
      institutionId,
    );
  }

  return fetch(
    buildApiUrl(endpoint),
    {
      ...options,

      headers,

      credentials:
        "include",
    },
  );
}


/* ========================================
   AUTHENTICATED FETCH
======================================== */

export async function apiFetch(
  endpoint: string,
  options: RequestInit = {},
) {
  let accessToken =
    getAccessToken();

  /*
    Caso a página seja recarregada
    sem access token, tenta recuperar
    usando o refresh HttpOnly.
  */

  if (!accessToken) {
    accessToken =
      await refreshAccessToken();
  }

  let response =
    await request(
      endpoint,
      accessToken,
      options,
    );

  /*
    Access expirou durante a sessão.
  */

  if (
    response.status !== 401
  ) {
    return response;
  }

  const freshAccessToken =
    await refreshAccessToken();

  if (!freshAccessToken) {
    return response;
  }

  response =
    await request(
      endpoint,
      freshAccessToken,
      options,
    );

  return response;
}


/* ========================================
   INSTITUTIONS
======================================== */

export async function getMyMemberships():
  Promise<Membership[]> {
  const response =
    await apiFetch(
      "/api/v1/institutions/mine/",
    );

  if (!response.ok) {
    throw new Error(
      "Não foi possível carregar as instituições.",
    );
  }

  const data:
    | Membership[]
    | {
        results?: Membership[];
      } =
    await response.json();

  /*
    Funciona tanto caso o DRF
    retorne lista normal quanto
    resposta paginada.
  */

  if (Array.isArray(data)) {
    return data;
  }

  if (
    data &&
    Array.isArray(
      data.results,
    )
  ) {
    return data.results;
  }

  return [];
}


export async function bootstrapInstitution() {
  const memberships =
    await getMyMemberships();

  /*
    Se já existe uma instituição
    armazenada, verificamos se o
    usuário ainda pertence a ela.
  */

  const previousInstitutionId =
    getActiveInstitutionId();

  if (
    previousInstitutionId
  ) {
    const previousMembership =
      memberships.find(
        (membership) =>
          membership.institution.id ===
          previousInstitutionId,
      );

    if (previousMembership) {
      saveActiveMembership(
        previousMembership,
      );

      return {
        memberships,

        activeMembership:
          previousMembership,

        requiresSelection:
          false,
      };
    }
  }

  /*
    Se só existe uma escola,
    selecionamos automaticamente.
  */

  if (
    memberships.length === 1
  ) {
    const membership =
      memberships[0];

    saveActiveMembership(
      membership,
    );

    return {
      memberships,

      activeMembership:
        membership,

      requiresSelection:
        false,
    };
  }

  /*
    Duas ou mais escolas:
    futuramente abriremos a tela
    de seleção de instituição.
  */

  clearActiveMembership();

  return {
    memberships,

    activeMembership: null,

    requiresSelection:
      memberships.length > 1,
  };
}


/* ========================================
   LOGOUT
======================================== */

export async function logout() {
  let accessToken =
    getAccessToken();

  try {
    if (!accessToken) {
      accessToken =
        await refreshAccessToken();
    }

    if (!accessToken) {
      return;
    }

    let response =
      await request(
        "/api/v1/auth/logout/",
        accessToken,
        {
          method: "POST",
        },
      );

    /*
      Se o access expirou exatamente
      antes do logout, recuperamos um
      token novo e tentamos novamente.

      Assim também conseguimos eliminar
      corretamente o refresh cookie
      no servidor.
    */

    if (
      response.status === 401
    ) {
      const freshAccessToken =
        await refreshAccessToken();

      if (freshAccessToken) {
        response =
          await request(
            "/api/v1/auth/logout/",
            freshAccessToken,
            {
              method: "POST",
            },
          );
      }
    }

    return response;
  } finally {
    clearSession();
  }
}