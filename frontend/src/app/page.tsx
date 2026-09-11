"use client";

import {
  CredentialResponse,
  GoogleLogin,
} from "@react-oauth/google";

import {
  FormEvent,
  useState,
} from "react";

import {
  useRouter,
} from "next/navigation";

import styles from "./login.module.css";


const API_URL =
  process.env
    .NEXT_PUBLIC_API_URL ?? "";


type NexusUser = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role:
    | "STUDENT"
    | "TEACHER"
    | "ADMIN";
  avatar: string | null;
  is_email_verified: boolean;
};


type AuthResponse = {
  access: string;
  user: NexusUser;
};


function getApiError(
  data: unknown,
) {
  if (
    typeof data === "object" &&
    data !== null
  ) {
    const response =
      data as Record<
        string,
        unknown
      >;


    if (
      typeof response.detail ===
      "string"
    ) {
      return response.detail;
    }


    const nonFieldErrors =
      response.non_field_errors;


    if (
      Array.isArray(
        nonFieldErrors,
      ) &&
      typeof nonFieldErrors[0] ===
        "string"
    ) {
      return nonFieldErrors[0];
    }
  }


  return (
    "Não foi possível realizar o acesso."
  );
}


function saveSession(
  data: AuthResponse,
) {
  sessionStorage.setItem(
    "nexus_access",
    data.access,
  );


  sessionStorage.setItem(
    "nexus_user",
    JSON.stringify(
      data.user,
    ),
  );
}


export default function Home() {
  const router =
    useRouter();


  const [
    email,
    setEmail,
  ] =
    useState("");


  const [
    password,
    setPassword,
  ] =
    useState("");


  const [
    loading,
    setLoading,
  ] =
    useState(false);


  const [
    googleLoading,
    setGoogleLoading,
  ] =
    useState(false);


  const [
    error,
    setError,
  ] =
    useState<string | null>(
      null,
    );


  async function handleLogin(
    event:
      FormEvent<HTMLFormElement>,
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
      const response =
        await fetch(
          `${API_URL}/api/v1/auth/login/`,
          {
            method: "POST",

            credentials:
              "include",

            headers: {
              "Content-Type":
                "application/json",
            },

            body:
              JSON.stringify({
                email,
                password,
              }),
          },
        );


      const data =
        await response.json();


      if (!response.ok) {
        setError(
          getApiError(data),
        );

        return;
      }


      saveSession(
        data as AuthResponse,
      );


      router.push(
        "/dashboard",
      );
    } catch {
      setError(
        "Não foi possível conectar ao Nexus Academy.",
      );
    } finally {
      setLoading(false);
    }
  }


  async function handleGoogleLogin(
    googleResponse:
      CredentialResponse,
  ) {
    if (!API_URL) {
      setError(
        "A URL da API não foi configurada.",
      );

      return;
    }


    if (
      !googleResponse.credential
    ) {
      setError(
        "O Google não retornou uma credencial válida.",
      );

      return;
    }


    setGoogleLoading(true);

    setError(null);


    try {
      const response =
        await fetch(
          `${API_URL}/api/v1/auth/google/`,
          {
            method: "POST",

            credentials:
              "include",

            headers: {
              "Content-Type":
                "application/json",
            },

            body:
              JSON.stringify({
                credential:
                  googleResponse
                    .credential,
              }),
          },
        );


      const data =
        await response.json();


      if (!response.ok) {
        setError(
          getApiError(data),
        );

        return;
      }


      saveSession(
        data as AuthResponse,
      );


      router.push(
        "/dashboard",
      );
    } catch {
      setError(
        "Não foi possível concluir o acesso com Google.",
      );
    } finally {
      setGoogleLoading(false);
    }
  }


  return (
    <main
      className={
        styles.page
      }
    >
      <section
        className={
          styles.hero
        }
      >
        <div
          className={
            styles.aurora
          }
          aria-hidden="true"
        >
          <span
            className={
              styles.auroraOne
            }
          />

          <span
            className={
              styles.auroraTwo
            }
          />

          <span
            className={
              styles.auroraThree
            }
          />
        </div>


        <div
          className={
            styles.grid
          }
          aria-hidden="true"
        />


        <div
          className={
            styles.noise
          }
          aria-hidden="true"
        />


        <header
          className={
            styles.brand
          }
        >
          <div
            className={
              styles.brandMark
            }
            aria-hidden="true"
          >
            N
          </div>

          <div
            className={
              styles.brandCopy
            }
          >
            <strong>
              Nexus Academy
            </strong>

            <span>
              Sistema acadêmico
            </span>
          </div>
        </header>


        <div
          className={
            styles.heroContent
          }
        >
          <div
            className={
              styles.visual
            }
            aria-hidden="true"
          >
            <span
              className={
                styles.orbitOuter
              }
            />

            <span
              className={
                styles.orbitMiddle
              }
            />

            <div
              className={
                styles.orbitInner
              }
            >
              <span
                className={
                  styles.orbitLogo
                }
              >
                N
              </span>
            </div>


            <span
              className={`${styles.dataLine} ${styles.lineOne}`}
            />

            <span
              className={`${styles.dataLine} ${styles.lineTwo}`}
            />

            <span
              className={`${styles.dataLine} ${styles.lineThree}`}
            />


            <div
              className={`${styles.floatCard} ${styles.cardOne}`}
            >
              <span>
                AMBIENTE
              </span>

              <strong>
                Tudo conectado.
              </strong>

              <p>
                Uma experiência
                acadêmica centralizada.
              </p>
            </div>


            <div
              className={`${styles.floatCard} ${styles.cardTwo}`}
            >
              <span>
                NEXUS
              </span>

              <div
                className={
                  styles.statusRow
                }
              >
                <i
                  className={
                    styles.statusDot
                  }
                />

                <strong>
                  Ambiente ativo
                </strong>
              </div>

              <p>
                Simples, rápido e
                organizado.
              </p>
            </div>
          </div>


          <div
            className={
              styles.heroCopy
            }
          >
            <div
              className={
                styles.edition
              }
            >
              <strong>
                2026
              </strong>

              <i />

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


            <p
              className={
                styles.lead
              }
            >
              Notas, frequência,
              disciplinas e rotina
              acadêmica em uma
              experiência criada para
              deixar tudo mais simples.
            </p>
          </div>
        </div>


        <div
          className={
            styles.features
          }
        >
          <article
            className={
              styles.feature
            }
          >
            <span>
              01
            </span>

            <p>
              Seu desempenho
              acadêmico sem precisar
              procurar informação em
              vários lugares.
            </p>
          </article>


          <article
            className={
              styles.feature
            }
          >
            <span>
              02
            </span>

            <p>
              Frequência e rotina
              sempre visíveis quando
              você precisar.
            </p>
          </article>


          <article
            className={
              styles.feature
            }
          >
            <span>
              03
            </span>

            <p>
              Alunos, professores e
              instituições dentro da
              mesma estrutura.
            </p>
          </article>
        </div>


        <footer
          className={
            styles.heroFooter
          }
        >
          <span>
            NXS — AL
          </span>

          <span>
            Ambiente acadêmico digital
          </span>
        </footer>
      </section>


      <section
        className={
          styles.access
        }
      >
        <header
          className={
            styles.accessTop
          }
        >
          <span>
            ACESSO INSTITUCIONAL
          </span>

          <span
            className={
              styles.accessContext
            }
          >
            NXS / PORTAL 2026
          </span>
        </header>


        <div
          className={
            styles.loginCard
          }
        >
          <div
            className={
              styles.loginHeading
            }
          >
            <span
              className={
                styles.loginNumber
              }
            >
              /01
            </span>

            <div>
              <h2>
                Entrar
              </h2>

              <p>
                Use suas credenciais
                para acessar o seu
                ambiente acadêmico.
              </p>
            </div>
          </div>


          <form
            className={
              styles.form
            }
            onSubmit={
              handleLogin
            }
          >
            <label
              className={
                styles.field
              }
            >
              <span
                className={
                  styles.fieldLabel
                }
              >
                E-mail institucional
              </span>

              <input
                className={
                  styles.input
                }
                type="email"
                placeholder="voce@academico.edu.br"
                autoComplete="email"
                value={email}
                onChange={(
                  event,
                ) =>
                  setEmail(
                    event
                      .target
                      .value,
                  )
                }
                required
              />
            </label>


            <label
              className={
                styles.field
              }
            >
              <div
                className={
                  styles.labelRow
                }
              >
                <span>
                  Senha
                </span>

                <button
                  type="button"
                  className={
                    styles.textButton
                  }
                >
                  Esqueci minha senha
                </button>
              </div>

              <input
                className={
                  styles.input
                }
                type="password"
                placeholder="••••••••"
                autoComplete="current-password"
                value={password}
                onChange={(
                  event,
                ) =>
                  setPassword(
                    event
                      .target
                      .value,
                  )
                }
                required
              />
            </label>


            {error && (
              <div
                className={
                  styles.error
                }
                role="alert"
              >
                <span
                  aria-hidden="true"
                >
                  !
                </span>

                <p>
                  {error}
                </p>
              </div>
            )}


            <button
              className={
                styles.primary
              }
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Verificando acesso..."
                : "Entrar no Nexus"}
            </button>
          </form>


          <div
            className={
              styles.divider
            }
          >
            <span />

            <p>
              ou
            </p>

            <span />
          </div>


          <div
            className={
              styles.google
            }
          >
            {googleLoading ? (
              <button
                className={
                  styles.googleLoading
                }
                type="button"
                disabled
              >
                Validando com
                Google...
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
                width="320"
                use_fedcm_for_button={
                  true
                }
              />
            )}
          </div>


          <p
            className={
              styles.note
            }
          >
            Acesso destinado a alunos,
            professores e
            administradores vinculados
            à instituição.
          </p>
        </div>


        <footer
          className={
            styles.accessFooter
          }
        >
          <span>
            © 2026 Nexus Academy
          </span>

          <div>
            <button
              type="button"
            >
              Privacidade
            </button>

            <button
              type="button"
            >
              Suporte
            </button>
          </div>
        </footer>
      </section>
    </main>
  );
}