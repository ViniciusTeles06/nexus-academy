"use client";

import { CredentialResponse, GoogleLogin } from "@react-oauth/google";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "";

type NexusUser = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: "STUDENT" | "TEACHER" | "ADMIN";
  avatar: string | null;
  is_email_verified: boolean;
};

type AuthResponse = {
  access: string;
  user: NexusUser;
};

function getApiError(data: unknown) {
  if (
    typeof data === "object" &&
    data !== null
  ) {
    const response = data as Record<
      string,
      unknown
    >;

    if (typeof response.detail === "string") {
      return response.detail;
    }

    const nonFieldErrors =
      response.non_field_errors;

    if (
      Array.isArray(nonFieldErrors) &&
      typeof nonFieldErrors[0] === "string"
    ) {
      return nonFieldErrors[0];
    }
  }

  return "Não foi possível realizar o acesso.";
}

function saveSession(data: AuthResponse) {
  sessionStorage.setItem(
    "nexus_access",
    data.access,
  );

  sessionStorage.setItem(
    "nexus_user",
    JSON.stringify(data.user),
  );
}

export default function Home() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [googleLoading, setGoogleLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  async function handleLogin(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!API_URL) {
      setError(
        "A URL da API não foi configurada.",
      );
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${API_URL}/api/v1/auth/login/`,
        {
          method: "POST",

          credentials: "include",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            email,
            password,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        setError(getApiError(data));
        return;
      }

      saveSession(
        data as AuthResponse,
      );

      router.push("/dashboard");
    } catch {
      setError(
        "Não foi possível conectar ao Nexus Academy.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleGoogleLogin(
    googleResponse: CredentialResponse,
  ) {
    if (!API_URL) {
      setError(
        "A URL da API não foi configurada.",
      );
      return;
    }

    if (!googleResponse.credential) {
      setError(
        "O Google não retornou uma credencial válida.",
      );
      return;
    }

    setGoogleLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${API_URL}/api/v1/auth/google/`,
        {
          method: "POST",

          credentials: "include",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            credential:
              googleResponse.credential,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        setError(getApiError(data));
        return;
      }

      saveSession(
        data as AuthResponse,
      );

      router.push("/dashboard");
    } catch {
      setError(
        "Não foi possível concluir o acesso com Google.",
      );
    } finally {
      setGoogleLoading(false);
    }
  }

  return (
    <main className="login-page">
      <section className="identity">
        <header className="brand">
          <div
            className="brand-symbol"
            aria-hidden="true"
          >
            N
          </div>

          <div className="brand-copy">
            <strong>Nexus Academy</strong>
            <span>Sistema acadêmico</span>
          </div>
        </header>

        <div className="identity-content">
          <div
            className="hero-art"
            aria-hidden="true"
          >
            <span className="hero-word">
              NEXUS
            </span>

            <span className="hero-rule rule-one" />
            <span className="hero-rule rule-two" />
            <span className="hero-rule rule-three" />

            <span className="hero-point point-one" />
            <span className="hero-point point-two" />
            <span className="hero-point point-three" />

            <span className="hero-coordinate coordinate-one">
              01 / NXS
            </span>

            <span className="hero-coordinate coordinate-two">
              ACAD / 26
            </span>
          </div>

          <div className="hero-copy">
            <div className="edition">
              <span>2026</span>
              <span>
                ACESSO ACADÊMICO
              </span>
            </div>

            <h1>
              Faculdade já exige
              <br />
              atenção demais.
              <br />

              <span>
                O sistema não deveria.
              </span>
            </h1>

            <p className="lead">
              Notas, frequência,
              disciplinas e rotina
              acadêmica sem precisar
              procurar informação em
              vários lugares.
            </p>
          </div>

          <div className="academic-notes">
            <article>
              <span>01</span>

              <p>
                Consulte suas notas sem
                abrir disciplina por
                disciplina.
              </p>
            </article>

            <article>
              <span>02</span>

              <p>
                Acompanhe sua frequência
                antes que uma falta vire
                problema.
              </p>
            </article>

            <article>
              <span>03</span>

              <p>
                Alunos, professores e
                administração dentro da
                mesma estrutura.
              </p>
            </article>
          </div>
        </div>

        <footer className="identity-footer">
          <span>NXS — AL</span>
          <span>
            Ambiente acadêmico digital
          </span>
        </footer>
      </section>

      <section className="access">
        <header className="access-top">
          <span>
            ACESSO INSTITUCIONAL
          </span>

          <span className="access-context">
            NXS / PORTAL 2026
          </span>
        </header>

        <div className="login-shell">
          <div className="login-heading">
            <span className="section-number">
              /01
            </span>

            <div>
              <h2>Entrar</h2>

              <p>
                Use suas credenciais para
                acessar o seu ambiente
                acadêmico.
              </p>
            </div>
          </div>

          <form
            className="login-form"
            onSubmit={handleLogin}
          >
            <label>
              <span>
                E-mail institucional
              </span>

              <input
                type="email"
                placeholder="voce@academico.edu.br"
                autoComplete="email"
                value={email}
                onChange={(event) =>
                  setEmail(
                    event.target.value,
                  )
                }
                required
              />
            </label>

            <label>
              <div className="label-row">
                <span>Senha</span>

                <button
                  type="button"
                  className="text-action"
                >
                  Esqueci minha senha
                </button>
              </div>

              <input
                type="password"
                placeholder="••••••••"
                autoComplete="current-password"
                value={password}
                onChange={(event) =>
                  setPassword(
                    event.target.value,
                  )
                }
                required
              />
            </label>

            {error && (
              <div
                className="login-error"
                role="alert"
              >
                <span aria-hidden="true">
                  !
                </span>

                <p>{error}</p>
              </div>
            )}

            <button
              className="primary-action"
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Verificando acesso..."
                : "Entrar no Nexus"}
            </button>
          </form>

          <div className="divider">
            <span />
            <p>ou</p>
            <span />
          </div>

          <div className="google-login">
            {googleLoading ? (
              <button
                className="google-loading"
                type="button"
                disabled
              >
                Validando com Google...
              </button>
            ) : (
              <GoogleLogin
                onSuccess={
                  handleGoogleLogin
                }
                onError={() =>
                  setError(
                    "Não foi possível iniciar o login com Google.",
                  )
                }
                theme="outline"
                size="large"
                text="continue_with"
                shape="rectangular"
                logo_alignment="left"
                width="400"
              />
            )}
          </div>

          <p className="access-note">
            Acesso destinado a alunos,
            professores e administradores
            vinculados à instituição.
          </p>
        </div>

        <footer className="access-footer">
          <span>
            © 2026 Nexus Academy
          </span>

          <div>
            <button type="button">
              Privacidade
            </button>

            <button type="button">
              Suporte
            </button>
          </div>
        </footer>
      </section>
    </main>
  );
}