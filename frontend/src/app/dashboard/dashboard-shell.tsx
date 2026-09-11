"use client";

import {
  useEffect,
  useMemo,
  useState,
  type MouseEvent,
  type ReactNode,
} from "react";

import Link from "next/link";

import {
  usePathname,
  useRouter,
} from "next/navigation";

import {
  apiFetch,
  bootstrapInstitution,
  clearSession,
  logout,
  type Membership,
} from "@/lib/api";

import {
  DashboardProvider,
  type DashboardUser,
} from "./dashboard-context";

import styles from "./dashboard-shell.module.css";


type DashboardShellProps = {
  children: ReactNode;
};


type NavIconName =
  | "overview"
  | "subjects"
  | "grades"
  | "attendance"
  | "agenda";


type NavItem = {
  href: string;
  label: string;
  number: string;
  icon: NavIconName;
};


const navItems: NavItem[] = [
  {
    href: "/dashboard",
    label: "Visão geral",
    number: "01",
    icon: "overview",
  },
  {
    href: "/dashboard/subjects",
    label: "Disciplinas",
    number: "02",
    icon: "subjects",
  },
  {
    href: "/dashboard/grades",
    label: "Notas",
    number: "03",
    icon: "grades",
  },
  {
    href: "/dashboard/attendance",
    label: "Frequência",
    number: "04",
    icon: "attendance",
  },
  {
    href: "/dashboard/agenda",
    label: "Agenda",
    number: "05",
    icon: "agenda",
  },
];


function getRoleLabel(
  membership: Membership,
) {
  if (
    membership.role ===
    "OWNER"
  ) {
    return "Proprietário";
  }

  if (
    membership.role ===
    "ADMIN"
  ) {
    return "Administrador";
  }

  if (
    membership.role ===
    "TEACHER"
  ) {
    return "Professor";
  }

  return "Aluno";
}


function getActiveIndex(
  pathname: string,
) {
  if (
    pathname.startsWith(
      "/dashboard/subjects",
    )
  ) {
    return 1;
  }

  if (
    pathname.startsWith(
      "/dashboard/grades",
    )
  ) {
    return 2;
  }

  if (
    pathname.startsWith(
      "/dashboard/attendance",
    )
  ) {
    return 3;
  }

  if (
    pathname.startsWith(
      "/dashboard/agenda",
    )
  ) {
    return 4;
  }

  return 0;
}


function getPageLabel(
  index: number,
) {
  return (
    navItems[index]?.label ??
    "Visão geral"
  );
}


function NavIcon({
  name,
}: {
  name: NavIconName;
}) {
  const props = {
    width: 18,
    height: 18,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.7,
    strokeLinecap:
      "round" as const,
    strokeLinejoin:
      "round" as const,
    "aria-hidden": true,
  };


  if (
    name === "overview"
  ) {
    return (
      <svg {...props}>
        <rect
          x="3"
          y="3"
          width="7"
          height="7"
          rx="2"
        />

        <rect
          x="14"
          y="3"
          width="7"
          height="7"
          rx="2"
        />

        <rect
          x="3"
          y="14"
          width="7"
          height="7"
          rx="2"
        />

        <rect
          x="14"
          y="14"
          width="7"
          height="7"
          rx="2"
        />
      </svg>
    );
  }


  if (
    name === "subjects"
  ) {
    return (
      <svg {...props}>
        <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H11v17H6.5A2.5 2.5 0 0 0 4 22Z" />

        <path d="M20 5.5A2.5 2.5 0 0 0 17.5 3H13v17h4.5A2.5 2.5 0 0 1 20 22Z" />
      </svg>
    );
  }


  if (
    name === "grades"
  ) {
    return (
      <svg {...props}>
        <path d="M5 4h14v16H5z" />

        <path d="M8 9h8" />

        <path d="M8 13h5" />

        <path d="m15 15 1.3 1.3L19 13.5" />
      </svg>
    );
  }


  if (
    name === "attendance"
  ) {
    return (
      <svg {...props}>
        <path d="M4 19V9" />

        <path d="M10 19V5" />

        <path d="M16 19v-7" />

        <path d="M22 19V3" />
      </svg>
    );
  }


  return (
    <svg {...props}>
      <rect
        x="3"
        y="5"
        width="18"
        height="16"
        rx="2"
      />

      <path d="M7 3v4" />

      <path d="M17 3v4" />

      <path d="M3 10h18" />

      <path d="M8 14h.01" />

      <path d="M12 14h.01" />

      <path d="M16 14h.01" />
    </svg>
  );
}


export default function DashboardShell({
  children,
}: DashboardShellProps) {
  const router =
    useRouter();

  const pathname =
    usePathname();


  const [
    user,
    setUser,
  ] =
    useState<
      DashboardUser | null
    >(null);


  const [
    membership,
    setMembership,
  ] =
    useState<
      Membership | null
    >(null);


  const [
    loading,
    setLoading,
  ] =
    useState(true);


  const [
    error,
    setError,
  ] =
    useState<
      string | null
    >(null);


  const [
    loggingOut,
    setLoggingOut,
  ] =
    useState(false);


  /*
   * O índice visual muda
   * imediatamente ao clique.
   *
   * Não esperamos o Next terminar
   * a navegação para mover o pill.
   */
  const [
    optimisticIndex,
    setOptimisticIndex,
  ] =
    useState(() =>
      getActiveIndex(
        pathname,
      ),
    );


  const actualIndex =
    useMemo(
      () =>
        getActiveIndex(
          pathname,
        ),
      [pathname],
    );


  /*
   * Quando a rota terminar de
   * trocar, sincronizamos o estado
   * visual com o endereço real.
   */
  useEffect(() => {
    setOptimisticIndex(
      actualIndex,
    );
  }, [actualIndex]);


  /*
   * ============================================
   * PREFETCH
   * ============================================
   *
   * Assim que o shell existe,
   * pedimos ao Next para preparar
   * todas as categorias.
   *
   * No clique, boa parte do código
   * já estará disponível.
   */
  useEffect(() => {
    navItems.forEach(
      (item) => {
        router.prefetch(
          item.href,
        );
      },
    );
  }, [router]);


  /*
   * ============================================
   * SESSION / INSTITUTION BOOTSTRAP
   * ============================================
   *
   * Como este componente pertence
   * ao layout do dashboard, ele
   * permanece montado durante a
   * navegação entre as categorias.
   *
   * Portanto usuário + instituição
   * não precisam carregar novamente.
   */
  useEffect(() => {
    let mounted = true;


    async function bootstrap() {
      try {
        const userResponse =
          await apiFetch(
            "/api/v1/auth/me/",
          );


        if (
          !userResponse.ok
        ) {
          clearSession();

          router.replace(
            "/",
          );

          return;
        }


        const userData =
          (await userResponse.json()) as DashboardUser;


        if (!mounted) {
          return;
        }


        setUser(
          userData,
        );


        const institutionState =
          await bootstrapInstitution();


        if (!mounted) {
          return;
        }


        if (
          institutionState
            .memberships
            .length === 0
        ) {
          setError(
            "Sua conta ainda não está vinculada a uma instituição.",
          );

          setLoading(
            false,
          );

          return;
        }


        if (
          institutionState
            .requiresSelection
        ) {
          setError(
            "Selecione uma instituição para continuar.",
          );

          setLoading(
            false,
          );

          return;
        }


        if (
          !institutionState
            .activeMembership
        ) {
          setError(
            "Não foi possível definir a instituição ativa.",
          );

          setLoading(
            false,
          );

          return;
        }


        const currentResponse =
          await apiFetch(
            "/api/v1/institutions/current/",
          );


        if (
          !currentResponse.ok
        ) {
          setError(
            "Não foi possível validar seu acesso à instituição.",
          );

          setLoading(
            false,
          );

          return;
        }


        const currentMembership =
          (await currentResponse.json()) as Membership;


        if (!mounted) {
          return;
        }


        setMembership(
          currentMembership,
        );

        setError(
          null,
        );

        setLoading(
          false,
        );
      } catch {
        if (!mounted) {
          return;
        }


        setError(
          "Não foi possível carregar seu ambiente acadêmico.",
        );

        setLoading(
          false,
        );
      }
    }


    void bootstrap();


    return () => {
      mounted = false;
    };
  }, [router]);


  /*
   * ============================================
   * NAVIGATION FEEDBACK
   * ============================================
   *
   * Isso não substitui o Link.
   * Apenas atualiza visualmente o
   * dashboard antes da troca de rota.
   */
  function handleNavClick(
    event:
      MouseEvent<HTMLAnchorElement>,
    index: number,
  ) {
    /*
     * Permite normalmente:
     * Ctrl + clique
     * Cmd + clique
     * Shift + clique
     * abrir em nova aba etc.
     */
    if (
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return;
    }


    setOptimisticIndex(
      index,
    );
  }


  function handleNavIntent(
    href: string,
  ) {
    /*
     * Desktop:
     * ao aproximar o mouse,
     * garantimos prefetch.
     *
     * Mobile:
     * o prefetch geral do efeito
     * acima já cobre os links.
     */
    router.prefetch(
      href,
    );
  }


  async function handleLogout() {
    setLoggingOut(
      true,
    );


    await logout();


    router.replace(
      "/",
    );


    router.refresh();
  }


  /*
   * ============================================
   * FIRST LOAD ONLY
   * ============================================
   *
   * Esse loading deve existir ao
   * entrar no dashboard.
   *
   * Ele NÃO deve reaparecer ao ir
   * de Notas para Frequência etc.
   */
  if (loading) {
    return (
      <main
        className={
          styles.loading
        }
      >
        <div
          className={
            styles.loadingHalo
          }
          aria-hidden="true"
        />

        <div
          className={
            styles.loadingMark
          }
        >
          N
        </div>

        <div
          className={
            styles.loadingTrack
          }
        >
          <span />
        </div>

        <p>
          Preparando seu ambiente
        </p>
      </main>
    );
  }


  if (
    error ||
    !user ||
    !membership
  ) {
    return (
      <main
        className={
          styles.loading
        }
      >
        <div
          className={
            styles.loadingMark
          }
        >
          N
        </div>

        <strong
          className={
            styles.errorTitle
          }
        >
          Ambiente indisponível
        </strong>

        <p>
          {error ??
            "Não foi possível iniciar o Nexus Academy."}
        </p>
      </main>
    );
  }


  const roleLabel =
    getRoleLabel(
      membership,
    );


  const institutionName =
    membership
      .institution
      .name;


  const name =
    user.first_name ||
    user.full_name ||
    user.email.split(
      "@",
    )[0];


  const initials =
    `${
      user.first_name?.[0] ??
      ""
    }${
      user.last_name?.[0] ??
      ""
    }` ||
    user.email[0]
      .toUpperCase();


  const visualPageLabel =
    getPageLabel(
      optimisticIndex,
    );


  return (
    <DashboardProvider
      value={{
        user,
        membership,
        institutionName,
        roleLabel,
      }}
    >
      <main
        className={
          styles.shell
        }
      >
        <div
          className={
            styles.ambient
          }
          aria-hidden="true"
        >
          <span
            className={
              styles.ambientOne
            }
          />

          <span
            className={
              styles.ambientTwo
            }
          />
        </div>


        <aside
          className={
            styles.sidebar
          }
        >
          <div
            className={
              styles.brand
            }
          >
            <div
              className={
                styles.brandMark
              }
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
          </div>


          <div
            className={
              styles.navigation
            }
          >
            <span
              className={
                styles.navigationLabel
              }
            >
              ACADÊMICO
            </span>


            <nav
              className={
                styles.nav
              }
              aria-label="Navegação acadêmica"
            >
              <span
                className={
                  styles.navIndicator
                }
                style={{
                  transform:
                    `translate3d(
                      0,
                      ${
                        optimisticIndex *
                        52
                      }px,
                      0
                    )`,
                }}
                aria-hidden="true"
              />


              {navItems.map(
                (
                  item,
                  index,
                ) => {
                  const isActive =
                    index ===
                    optimisticIndex;


                  return (
                    <Link
                      key={
                        item.href
                      }
                      href={
                        item.href
                      }
                      prefetch={
                        true
                      }
                      className={`${styles.navLink} ${
                        isActive
                          ? styles.navLinkActive
                          : ""
                      }`}
                      aria-current={
                        isActive
                          ? "page"
                          : undefined
                      }
                      onClick={(
                        event,
                      ) =>
                        handleNavClick(
                          event,
                          index,
                        )
                      }
                      onMouseEnter={() =>
                        handleNavIntent(
                          item.href,
                        )
                      }
                      onFocus={() =>
                        handleNavIntent(
                          item.href,
                        )
                      }
                      onTouchStart={() =>
                        handleNavIntent(
                          item.href,
                        )
                      }
                    >
                      <span
                        className={
                          styles.navNumber
                        }
                      >
                        {
                          item.number
                        }
                      </span>

                      <span
                        className={
                          styles.navIcon
                        }
                      >
                        <NavIcon
                          name={
                            item.icon
                          }
                        />
                      </span>

                      <span
                        className={
                          styles.navText
                        }
                      >
                        {
                          item.label
                        }
                      </span>
                    </Link>
                  );
                },
              )}
            </nav>
          </div>


          <div
            className={
              styles.account
            }
          >
            <div
              className={
                styles.accountCard
              }
            >
              <div
                className={
                  styles.avatar
                }
              >
                {user.avatar ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={
                      user.avatar
                    }
                    alt=""
                  />
                ) : (
                  <span>
                    {initials}
                  </span>
                )}
              </div>

              <div
                className={
                  styles.accountCopy
                }
              >
                <strong>
                  {name}
                </strong>

                <span>
                  {roleLabel}
                </span>
              </div>
            </div>


            <button
              type="button"
              className={
                styles.logout
              }
              disabled={
                loggingOut
              }
              onClick={
                handleLogout
              }
            >
              {loggingOut
                ? "Encerrando..."
                : "Encerrar sessão"}
            </button>
          </div>
        </aside>


        <section
          className={
            styles.main
          }
        >
          <header
            className={
              styles.topbar
            }
          >
            <div
              className={
                styles.topbarPath
              }
            >
              <span>
                NXS
              </span>

              <i />

              <strong>
                {
                  visualPageLabel
                }
              </strong>
            </div>


            <div
              className={
                styles.topbarMeta
              }
            >
              <span>
                {
                  institutionName
                }
              </span>

              <i />

              <span>
                {
                  roleLabel
                }
              </span>
            </div>
          </header>


          {/*
            IMPORTANTE:

            Antes existia:

            key={pathname}

            Isso fazia o wrapper do
            conteúdo ser recriado a
            cada troca de rota.

            Agora ele permanece
            estável e somente o
            children muda.
          */}
          <div
            className={
              styles.routeFrame
            }
          >
            {children}
          </div>
        </section>


        <nav
          className={
            styles.mobileDock
          }
          aria-label="Navegação acadêmica"
        >
          <span
            className={
              styles.mobileIndicator
            }
            style={{
              transform:
                `translate3d(
                  ${
                    optimisticIndex *
                    100
                  }%,
                  0,
                  0
                )`,
            }}
            aria-hidden="true"
          />


          {navItems.map(
            (
              item,
              index,
            ) => {
              const isActive =
                index ===
                optimisticIndex;


              return (
                <Link
                  key={
                    item.href
                  }
                  href={
                    item.href
                  }
                  prefetch={
                    true
                  }
                  className={`${styles.mobileLink} ${
                    isActive
                      ? styles.mobileLinkActive
                      : ""
                  }`}
                  aria-current={
                    isActive
                      ? "page"
                      : undefined
                  }
                  onClick={(
                    event,
                  ) =>
                    handleNavClick(
                      event,
                      index,
                    )
                  }
                  onTouchStart={() =>
                    handleNavIntent(
                      item.href,
                    )
                  }
                >
                  <span
                    className={
                      styles.mobileIcon
                    }
                  >
                    <NavIcon
                      name={
                        item.icon
                      }
                    />
                  </span>

                  <span>
                    {
                      item.label
                    }
                  </span>
                </Link>
              );
            },
          )}
        </nav>
      </main>
    </DashboardProvider>
  );
}