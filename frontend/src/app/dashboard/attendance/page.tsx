"use client";

import DashboardVisual from "../dashboard-visuals";

import {
  useDashboard,
} from "../dashboard-context";

import styles from "./attendance.module.css";


export default function AttendancePage() {
  const {
    institutionName,
  } =
    useDashboard();


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
              /04
            </span>

            <i />

            <span>
              FREQUÊNCIA
            </span>
          </div>


          <h1>
            Presença
            <br />

            <span>
              sob controle.
            </span>
          </h1>


          <p
            className={
              styles.lead
            }
          >
            Acompanhe sua frequência
            por disciplina, veja
            registros de aula e
            mantenha sua presença
            acadêmica sempre visível.
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
            type="attendance"
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
              NXS / 04
            </span>

            <h2>
              Sua frequência
            </h2>
          </div>

          <p>
            Os registros de presença
            serão exibidos assim que
            houver sessões de aula
            vinculadas ao seu perfil.
          </p>
        </header>


        <div
          className={
            styles.attendanceGrid
          }
        >
          <article
            className={
              styles.primaryCard
            }
          >
            <div
              className={
                styles.cardHeader
              }
            >
              <span>
                PRESENÇA GERAL
              </span>

              <span>
                01
              </span>
            </div>


            <strong>
              —
            </strong>


            <div
              className={
                styles.progressTrack
              }
            >
              <span />
            </div>


            <p>
              Ainda não existem
              registros suficientes
              para calcular sua
              frequência.
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
                AULAS
              </span>

              <span>
                02
              </span>
            </div>


            <strong>
              0
            </strong>


            <p>
              Nenhuma sessão de aula
              registrada ainda.
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
                REGISTROS
              </span>

              <span>
                03
              </span>
            </div>


            <strong>
              —
            </strong>


            <p>
              Os registros aparecerão
              aqui conforme as aulas
              forem cadastradas.
            </p>
          </article>
        </div>


        <div
          className={
            styles.emptyState
          }
        >
          <div
            className={
              styles.emptyVisual
            }
          >
            <div
              className={
                styles.emptyRing
              }
            >
              <span />

              <span />

              <span />

              <div>
                <strong>
                  %
                </strong>

                <small>
                  PRESENÇA
                </small>
              </div>
            </div>
          </div>


          <div
            className={
              styles.emptyCopy
            }
          >
            <span>
              HISTÓRICO DE PRESENÇA
            </span>

            <h3>
              Cada aula vai contar.
            </h3>

            <p>
              Quando os professores
              começarem a registrar
              as aulas, você poderá
              acompanhar sua presença
              disciplina por
              disciplina.
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
          Frequência / NXS 04
        </span>
      </footer>
    </div>
  );
}