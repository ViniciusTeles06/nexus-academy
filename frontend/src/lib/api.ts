const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "";

const ACCESS_KEY = "nexus_access";
const USER_KEY = "nexus_user";

export function getAccessToken() {
  if (typeof window === "undefined") {
    return null;
  }

  return sessionStorage.getItem(ACCESS_KEY);
}

export function saveAccessToken(access: string) {
  sessionStorage.setItem(ACCESS_KEY, access);
}

export function saveUser(user: unknown) {
  sessionStorage.setItem(
    USER_KEY,
    JSON.stringify(user),
  );
}

export function clearSession() {
  sessionStorage.removeItem(ACCESS_KEY);
  sessionStorage.removeItem(USER_KEY);
}

export async function refreshAccessToken() {
  if (!API_URL) {
    return null;
  }

  try {
    const response = await fetch(
      `${API_URL}/api/v1/auth/refresh/`,
      {
        method: "POST",
        credentials: "include",
      },
    );

    if (!response.ok) {
      clearSession();
      return null;
    }

    const data = (await response.json()) as {
      access?: string;
    };

    if (!data.access) {
      clearSession();
      return null;
    }

    saveAccessToken(data.access);

    return data.access;
  } catch {
    return null;
  }
}

async function request(
  path: string,
  token: string | null,
  options: RequestInit,
) {
  const headers = new Headers(options.headers);

  if (token) {
    headers.set(
      "Authorization",
      `Bearer ${token}`,
    );
  }

  return fetch(`${API_URL}${path}`, {
    ...options,
    headers,
    credentials: "include",
  });
}

export async function apiFetch(
  path: string,
  options: RequestInit = {},
) {
  let access = getAccessToken();

  if (!access) {
    access = await refreshAccessToken();
  }

  let response = await request(
    path,
    access,
    options,
  );

  if (response.status === 401) {
    access = await refreshAccessToken();

    if (!access) {
      return response;
    }

    response = await request(
      path,
      access,
      options,
    );
  }

  return response;
}

export async function logout() {
  const access = getAccessToken();

  try {
    await request(
      "/api/v1/auth/logout/",
      access,
      {
        method: "POST",
      },
    );
  } finally {
    clearSession();
  }
}