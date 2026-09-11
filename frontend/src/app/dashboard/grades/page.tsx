"use client";

import DashboardVisual from "../dashboard-visuals";

import {
  useDashboard,
} from "../dashboard-context";

import styles from "./grades.module.css";


export default function GradesPage() {
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
              /03
            </span>

            <i />

            <span>
              NOTAS
            </span>
          </div>


          <h1>
            Seu desempenho,
            <br />

            <span>
              sem mistério.
            </span>
          </h1>


          <p
            className={
              styles.lead
            }
          >
            Acompanhe avaliações,
            médias e evolução
            acadêmica com clareza,
            disciplina por disciplina.
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
            type="grades"
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
              NXS / 03
            </span>

            <h2>
              Desempenho acadêmico
            </h2>
          </div>

          <p>
            Suas médias e avaliações
            aparecerão aqui assim que
            forem registradas pela
            instituição.
          </p>
        </header>


        <div
          className={
            styles.gradeGrid
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
                MÉDIA DO PERÍODO
              </span>

              <span>
                01
              </span>
            </div>

            <strong>
              —
            </strong>

            <p>
              Ainda não existem
              avaliações registradas
              para calcular sua média.
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
                AVALIAÇÕES
              </span>

              <span>
                02
              </span>
            </div>

            <strong>
              0
            </strong>

            <p>
              Nenhuma avaliação
              disponível no momento.
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
                DISCIPLINAS
              </span>

              <span>
                03
              </span>
            </div>

            <strong>
              —
            </strong>

            <p>
              O vínculo das disciplinas
              ainda não foi carregado.
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
              styles.emptyGraph
            }
          >
            <span />

            <span />

            <span />

            <span />

            <i />
          </div>


          <div
            className={
              styles.emptyCopy
            }
          >
            <span>
              HISTÓRICO DE NOTAS
            </span>

            <h3>
              Seus resultados vão
              ganhar forma aqui.
            </h3>

            <p>
              Quando professores
              publicarem avaliações,
              você poderá acompanhar
              cada resultado e a
              evolução ao longo do
              período.
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
          Notas / NXS 03
        </span>
      </footer>
    </div>
  );
}