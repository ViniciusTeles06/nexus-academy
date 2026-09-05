"use client";

import {
  useEffect,
  useRef,
  useState,
} from "react";

import { useRouter } from "next/navigation";

import {
  apiFetch,
  clearSession,
  logout,
} from "@/lib/api";

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

type NavIconName =
  | "home"
  | "subjects"
  | "grades"
  | "attendance"
  | "agenda";

const navItems: {
  id: string;
  label: string;
  number: string;
  icon: NavIconName;
}[] = [
  {
    id: "overview",
    label: "Início",
    number: "01",
    icon: "home",
  },
  {
    id: "subjects",
    label: "Disciplinas",
    number: "02",
    icon: "subjects",
  },
  {
    id: "grades",
    label: "Notas",
    number: "03",
    icon: "grades",
  },
  {
    id: "attendance",
    label: "Frequência",
    number: "04",
    icon: "attendance",
  },
  {
    id: "agenda",
    label: "Agenda",
    number: "05",
    icon: "agenda",
  },
];

function getGreeting() {
  const hour = new Date().getHours();

  if (hour < 12) return "Bom dia";
  if (hour < 18) return "Boa tarde";

  return "Boa noite";
}

function getCurrentDate() {
  const date = new Date();

  const day = new Intl.DateTimeFormat(
    "pt-BR",
    {
      day: "2-digit",
    },
  ).format(date);

  const month = new Intl.DateTimeFormat(
    "pt-BR",
    {
      month: "short",
    },
  )
    .format(date)
    .replace(".", "")
    .toUpperCase();

  const weekday =
    new Intl.DateTimeFormat(
      "pt-BR",
      {
        weekday: "long",
      },
    )
      .format(date)
      .toUpperCase();

  return {
    day,
    month,
    weekday,
  };
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

  if (name === "home") {
    return (
      <svg {...props}>
        <path d="M3.5 10.5 12 3l8.5 7.5" />
        <path d="M5.5 9v11h13V9" />
        <path d="M9.5 20v-6h5v6" />
      </svg>
    );
  }

  if (name === "subjects") {
    return (
      <svg {...props}>
        <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H11v17H6.5A2.5 2.5 0 0 0 4 22Z" />
        <path d="M20 5.5A2.5 2.5 0 0 0 17.5 3H13v17h4.5A2.5 2.5 0 0 1 20 22Z" />
      </svg>
    );
  }

  if (name === "grades") {
    return (
      <svg {...props}>
        <path d="M5 4h14v16H5z" />
        <path d="M8 9h8" />
        <path d="M8 13h5" />
        <path d="m15 15 1.3 1.3L19 13.5" />
      </svg>
    );
  }

  if (name === "attendance") {
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

export default function Dashboard() {
  const router = useRouter();

  const [user, setUser] =
    useState<NexusUser | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [loggingOut, setLoggingOut] =
    useState(false);

  const [activeIndex, setActiveIndex] =
    useState(0);

  /*
    Evita que o IntersectionObserver
    dispute o controle da navegação
    durante um clique.
  */
  const navigationLock =
    useRef(false);

  const navigationTimer =
    useRef<ReturnType<
      typeof setTimeout
    > | null>(null);

  const date = getCurrentDate();

  /*
    Depois isso virá da API.
  */
  const hasAgendaNotice = false;

  useEffect(() => {
    let active = true;

    async function loadUser() {
      try {
        const response =
          await apiFetch(
            "/api/v1/auth/me/",
          );

        if (!response.ok) {
          clearSession();

          router.replace("/");

          return;
        }

        const data =
          (await response.json()) as NexusUser;

        if (active) {
          setUser(data);
          setLoading(false);
        }
      } catch {
        clearSession();

        router.replace("/");
      }
    }

    void loadUser();

    return () => {
      active = false;
    };
  }, [router]);

  /*
    Observer da seção visível.

    Ele funciona quando o usuário
    rola a página manualmente.

    Durante uma navegação por clique,
    navigationLock.current fica true,
    então não há disputa pelo activeIndex.
  */
  useEffect(() => {
    if (!user) return;

    const sections =
      navItems
        .map((item) =>
          document.getElementById(
            item.id,
          ),
        )
        .filter(
          (
            section,
          ): section is HTMLElement =>
            section !== null,
        );

    const observer =
      new IntersectionObserver(
        (entries) => {
          if (
            navigationLock.current
          ) {
            return;
          }

          const visible =
            entries
              .filter(
                (entry) =>
                  entry.isIntersecting,
              )
              .sort(
                (a, b) =>
                  b.intersectionRatio -
                  a.intersectionRatio,
              )[0];

          if (!visible) {
            return;
          }

          const index =
            navItems.findIndex(
              (item) =>
                item.id ===
                visible.target.id,
            );

          if (index >= 0) {
            setActiveIndex(index);
          }
        },
        {
          rootMargin:
            "-20% 0px -58% 0px",

          threshold: [
            0.05,
            0.15,
            0.3,
            0.5,
          ],
        },
      );

    sections.forEach(
      (section) => {
        observer.observe(section);
      },
    );

    return () => {
      observer.disconnect();
    };
  }, [user]);

  /*
    Limpa qualquer timer se
    o componente for desmontado.
  */
  useEffect(() => {
    return () => {
      if (
        navigationTimer.current
      ) {
        clearTimeout(
          navigationTimer.current,
        );
      }
    };
  }, []);

  function navigateTo(
    index: number,
  ) {
    navigationLock.current = true;

    if (
      navigationTimer.current
    ) {
      clearTimeout(
        navigationTimer.current,
      );
    }

    setActiveIndex(index);

    const section =
      document.getElementById(
        navItems[index].id,
      );

    section?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });

    navigationTimer.current =
      setTimeout(() => {
        navigationLock.current =
          false;

        navigationTimer.current =
          null;
      }, 900);
  }

  async function handleLogout() {
    setLoggingOut(true);

    await logout();

    router.replace("/");
    router.refresh();
  }

  if (loading) {
    return (
      <main className="nexus-loading">
        <div className="nexus-loading-mark">
          N
        </div>

        <div className="nexus-loading-line">
          <span />
        </div>

        <p>
          Preparando seu ambiente
          acadêmico
        </p>
      </main>
    );
  }

  if (!user) {
    return null;
  }

  const name =
    user.first_name ||
    user.full_name ||
    user.email.split("@")[0];

  const initials =
    `${user.first_name?.[0] ?? ""}${
      user.last_name?.[0] ?? ""
    }` ||
    user.email[0].toUpperCase();

  return (
    <main className="student-dashboard">
      <aside className="nexus-sidebar">
        <div className="nexus-sidebar-brand">
          <div className="nexus-sidebar-logo">
            N
          </div>

          <div>
            <strong>
              Nexus Academy
            </strong>

            <span>
              Sistema acadêmico
            </span>
          </div>
        </div>

        <div className="nexus-nav-wrapper">
          <span className="nexus-nav-label">
            ACADÊMICO
          </span>

          <nav className="nexus-desktop-nav">
            <span
              className="desktop-pill-indicator"
              style={{
                transform: `translate3d(
                  0,
                  ${
                    activeIndex *
                    48
                  }px,
                  0
                )`,
              }}
            />

            {navItems.map(
              (
                item,
                index,
              ) => (
                <button
                  key={item.id}
                  type="button"
                  className={
                    activeIndex ===
                    index
                      ? "active"
                      : ""
                  }
                  onClick={() =>
                    navigateTo(
                      index,
                    )
                  }
                >
                  <span className="nav-number">
                    {
                      item.number
                    }
                  </span>

                  <span className="nav-icon">
                    <NavIcon
                      name={
                        item.icon
                      }
                    />

                    {item.id ===
                      "agenda" &&
                      hasAgendaNotice && (
                        <i className="notification-dot" />
                      )}
                  </span>

                  <span className="nav-text">
                    {
                      item.label
                    }
                  </span>
                </button>
              ),
            )}
          </nav>
        </div>

        <div className="nexus-sidebar-account">
          <button
            type="button"
            className="account-button"
          >
            <div className="account-avatar">
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

            <div>
              <strong>
                {name}
              </strong>

              <span>
                Aluno
              </span>
            </div>
          </button>

          <button
            type="button"
            className="nexus-logout"
            onClick={
              handleLogout
            }
            disabled={
              loggingOut
            }
          >
            {loggingOut
              ? "Encerrando..."
              : "Encerrar sessão"}
          </button>
        </div>
      </aside>

      <section className="nexus-dashboard-main">
        <header className="nexus-topbar">
          <span>
            NXS / PORTAL ACADÊMICO
          </span>

          <div>
            <span>
              CONTA{" "}
              {user.is_email_verified
                ? "VERIFICADA"
                : "NÃO VERIFICADA"}
            </span>

            <i />

            <span>
              {user.role}
            </span>
          </div>
        </header>

        <div className="nexus-dashboard-content">
          <section
            className="nexus-overview"
            id="overview"
          >
            <div className="overview-copy">
              <div className="overview-eyebrow">
                <span>
                  /01
                </span>

                <span>
                  VISÃO GERAL
                </span>
              </div>

              <h1>
                {getGreeting()},
                <br />

                <em>
                  {name}.
                </em>
              </h1>

              <p>
                Seu dia acadêmico
                começa aqui.
                Informação
                essencial, sem
                ruído.
              </p>
            </div>

            <aside className="today-panel">
              <div className="today-header">
                <span>
                  HOJE
                </span>

                <span>
                  NXS / 01
                </span>
              </div>

              <div className="today-date">
                <strong
                  suppressHydrationWarning
                >
                  {date.day}
                </strong>

                <div>
                  <span
                    suppressHydrationWarning
                  >
                    {date.month}
                  </span>

                  <p
                    suppressHydrationWarning
                  >
                    {
                      date.weekday
                    }
                  </p>
                </div>
              </div>

              <div className="today-status">
                <span />

                <div>
                  <strong>
                    Agenda
                    disponível
                  </strong>

                  <p>
                    Nenhum
                    compromisso
                    acadêmico
                    sincronizado
                    ainda.
                  </p>
                </div>
              </div>
            </aside>
          </section>

          <section className="period-strip">
            <article>
              <span className="period-index">
                01
              </span>

              <span className="period-label">
                CURSO
              </span>

              <strong>
                Ainda não
                vinculado
              </strong>

              <p>
                Perfil acadêmico
                aguardando
                associação
                institucional.
              </p>
            </article>

            <article>
              <span className="period-index">
                02
              </span>

              <span className="period-label">
                PERÍODO ATUAL
              </span>

              <strong>
                —
              </strong>

              <p>
                Será exibido
                após o vínculo
                da matrícula.
              </p>
            </article>

            <article>
              <span className="period-index">
                03
              </span>

              <span className="period-label">
                MATRÍCULA
              </span>

              <strong>
                —
              </strong>

              <p>
                Nenhuma
                matrícula
                acadêmica
                associada.
              </p>
            </article>
          </section>

          <section
            className="live-section"
            id="subjects"
          >
            <header className="live-section-header">
              <div>
                <span>
                  /02
                </span>

                <h2>
                  Disciplinas
                </h2>
              </div>

              <p>
                Tudo que você
                está cursando
                no período
                atual.
              </p>
            </header>

            <div className="subjects-empty">
              <div className="empty-visual">
                <span>
                  02
                </span>

                <div>
                  <i />
                  <i />
                  <i />
                </div>
              </div>

              <div className="empty-copy">
                <span>
                  NENHUMA
                  DISCIPLINA
                </span>

                <h3>
                  Seu espaço
                  acadêmico
                  começa vazio.
                </h3>

                <p>
                  Assim que sua
                  matrícula for
                  vinculada, suas
                  disciplinas
                  aparecerão aqui
                  automaticamente.
                </p>
              </div>
            </div>
          </section>

          <section
            className="live-section"
            id="grades"
          >
            <header className="live-section-header">
              <div>
                <span>
                  /03
                </span>

                <h2>
                  Notas
                </h2>
              </div>

              <p>
                Seu desempenho,
                organizado por
                avaliação e
                disciplina.
              </p>
            </header>

            <div className="grade-layout">
              <article className="grade-main">
                <span>
                  MÉDIA DO
                  PERÍODO
                </span>

                <strong>
                  —
                </strong>

                <p>
                  Ainda não
                  existem
                  avaliações
                  registradas.
                </p>
              </article>

              <article className="grade-secondary">
                <div>
                  <span>
                    AVALIAÇÕES
                  </span>

                  <strong>
                    0
                  </strong>
                </div>

                <div className="grade-lines">
                  <i />
                  <i />
                  <i />
                </div>
              </article>
            </div>
          </section>

          <section
            className="live-section"
            id="attendance"
          >
            <header className="live-section-header">
              <div>
                <span>
                  /04
                </span>

                <h2>
                  Frequência
                </h2>
              </div>

              <p>
                Presença não
                deveria ser uma
                surpresa no fim
                do semestre.
              </p>
            </header>

            <div className="attendance-layout">
              <div className="attendance-big">
                <strong>
                  —
                </strong>

                <span>
                  FREQUÊNCIA
                  GERAL
                </span>
              </div>

              <div className="attendance-progress">
                <div className="progress-header">
                  <span>
                    REGISTROS
                  </span>

                  <span>
                    —
                  </span>
                </div>

                <div className="progress-track">
                  <span />
                </div>

                <p>
                  Os registros
                  de presença
                  serão exibidos
                  assim que
                  houver sessões
                  de aula
                  associadas ao
                  seu perfil.
                </p>
              </div>
            </div>
          </section>

          <section
            className="live-section"
            id="agenda"
          >
            <header className="live-section-header">
              <div>
                <span>
                  /05
                </span>

                <h2>
                  Agenda
                </h2>
              </div>

              <p>
                Avaliações,
                atividades e
                compromissos
                acadêmicos.
              </p>
            </header>

            <div className="agenda-empty">
              <div className="agenda-date-mark">
                <span
                  suppressHydrationWarning
                >
                  {date.month}
                </span>

                <strong
                  suppressHydrationWarning
                >
                  {date.day}
                </strong>
              </div>

              <div>
                <span>
                  PRÓXIMOS
                  COMPROMISSOS
                </span>

                <h3>
                  Sua agenda
                  está livre.
                </h3>

                <p>
                  Quando
                  avaliações ou
                  atividades
                  forem
                  cadastradas,
                  elas aparecerão
                  aqui.
                </p>
              </div>
            </div>
          </section>
        </div>

        <footer className="nexus-dashboard-footer">
          <span>
            © 2026 NEXUS
            ACADEMY
          </span>

          <span>
            AMBIENTE
            ACADÊMICO DIGITAL
          </span>
        </footer>
      </section>

      <nav className="nexus-mobile-dock">
        <span
          className="mobile-pill-indicator"
          style={{
            transform: `translate3d(
              ${
                activeIndex *
                100
              }%,
              0,
              0
            )`,
          }}
        />

        {navItems.map(
          (
            item,
            index,
          ) => (
            <button
              key={item.id}
              type="button"
              className={
                activeIndex ===
                index
                  ? "active"
                  : ""
              }
              onClick={() =>
                navigateTo(
                  index,
                )
              }
            >
              <span className="mobile-nav-icon">
                <NavIcon
                  name={
                    item.icon
                  }
                />

                {item.id ===
                  "agenda" &&
                  hasAgendaNotice && (
                    <i className="notification-dot" />
                  )}
              </span>

              <span>
                {item.label}
              </span>
            </button>
          ),
        )}
      </nav>
    </main>
  );
}