"use client";

import DashboardVisual from "../dashboard-visuals";

import {
  useDashboard,
} from "../dashboard-context";

import styles from "./agenda.module.css";


function getCurrentDate() {
  const date =
    new Date();

  const day =
    new Intl.DateTimeFormat(
      "pt-BR",
      {
        day: "2-digit",
      },
    ).format(date);

  const month =
    new Intl.DateTimeFormat(
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


export default function AgendaPage() {
  const {
    institutionName,
  } =
    useDashboard();

  const date =
    getCurrentDate();


  return (
    <div
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
            styles.heroCopy
          }
        >
          <div
            className={
              styles.eyebrow
            }
          >
            <span>
              /05
            </span>

            <i />

            <span>
              AGENDA
            </span>
          </div>


          <h1>
            Tudo no
            <br />

            <span>
              tempo certo.
            </span>
          </h1>


          <p
            className={
              styles.lead
            }
          >
            Avaliações, atividades,
            aulas e compromissos
            acadêmicos organizados
            em uma linha do tempo
            simples de acompanhar.
          </p>


          <div
            className={
              styles.context
            }
          >
            <span>
              INSTITUIÇÃO ATIVA
            </span>

            <strong>
              {
                institutionName
              }
            </strong>
          </div>
        </div>


        <div
          className={
            styles.heroVisual
          }
        >
          <DashboardVisual
            type="agenda"
          />
        </div>
      </section>


      <section
        className={
          styles.content
        }
      >
        <header
          className={
            styles.sectionHeader
          }
        >
          <div>
            <span>
              NXS / 05
            </span>

            <h2>
              Sua agenda
            </h2>
          </div>

          <p>
            Seus próximos eventos
            acadêmicos aparecerão aqui
            assim que forem cadastrados
            pela instituição.
          </p>
        </header>


        <div
          className={
            styles.agendaGrid
          }
        >
          <article
            className={
              styles.todayCard
            }
          >
            <div
              className={
                styles.cardHeader
              }
            >
              <span>
                HOJE
              </span>

              <span>
                01
              </span>
            </div>


            <div
              className={
                styles.dateBlock
              }
            >
              <strong
                suppressHydrationWarning
              >
                {date.day}
              </strong>

              <div>
                <span
                  suppressHydrationWarning
                >
                  {
                    date.month
                  }
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


            <div
              className={
                styles.todayStatus
              }
            >
              <i />

              <div>
                <strong>
                  Agenda livre
                </strong>

                <p>
                  Nenhum compromisso
                  acadêmico registrado
                  para hoje.
                </p>
              </div>
            </div>
          </article>


          <article
            className={
              styles.statCard
            }
          >
            <div
              className={
                styles.cardHeader
              }
            >
              <span>
                PRÓXIMOS EVENTOS
              </span>

              <span>
                02
              </span>
            </div>

            <strong>
              0
            </strong>

            <p>
              Nenhum evento futuro
              sincronizado ainda.
            </p>
          </article>


          <article
            className={
              styles.statCard
            }
          >
            <div
              className={
                styles.cardHeader
              }
            >
              <span>
                ATIVIDADES
              </span>

              <span>
                03
              </span>
            </div>

            <strong>
              —
            </strong>

            <p>
              As atividades aparecerão
              conforme forem cadastradas.
            </p>
          </article>
        </div>


        <div
          className={
            styles.timelineSection
          }
        >
          <div
            className={
              styles.timelineVisual
            }
          >
            <span
              className={
                styles.timelineLine
              }
            />

            <div
              className={`${styles.timelinePoint} ${styles.pointOne}`}
            >
              <i />

              <span>
                AGORA
              </span>
            </div>

            <div
              className={`${styles.timelinePoint} ${styles.pointTwo}`}
            >
              <i />

              <span>
                PRÓXIMO
              </span>
            </div>

            <div
              className={`${styles.timelinePoint} ${styles.pointThree}`}
            >
              <i />

              <span>
                FUTURO
              </span>
            </div>
          </div>


          <div
            className={
              styles.emptyCopy
            }
          >
            <span>
              LINHA DO TEMPO
            </span>

            <h3>
              Seus compromissos
              vão aparecer aqui.
            </h3>

            <p>
              Quando avaliações,
              atividades ou eventos
              forem registrados, a
              agenda vai organizar tudo
              em ordem cronológica.
            </p>
          </div>
        </div>
      </section>


      <footer
        className={
          styles.footer
        }
      >
        <span>
          © 2026 Nexus Academy
        </span>

        <span>
          Agenda / NXS 05
        </span>
      </footer>
    </div>
  );
}