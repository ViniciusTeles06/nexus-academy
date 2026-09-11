"use client";

import DashboardVisual from "../dashboard-visuals";

import {
  useDashboard,
} from "../dashboard-context";

import styles from "./subjects.module.css";


export default function SubjectsPage() {
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
              /02
            </span>

            <i />

            <span>
              DISCIPLINAS
            </span>
          </div>


          <h1>
            Tudo que você
            <br />

            <span>
              está cursando.
            </span>
          </h1>


          <p
            className={
              styles.lead
            }
          >
            Suas disciplinas,
            conteúdos e vínculos
            acadêmicos organizados em
            um único lugar.
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
            type="subjects"
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
              NXS / 02
            </span>

            <h2>
              Suas disciplinas
            </h2>
          </div>

          <p>
            Quando sua matrícula
            estiver vinculada, as
            disciplinas aparecerão
            automaticamente aqui.
          </p>
        </header>


        <div
          className={
            styles.emptyState
          }
        >
          <div
            className={
              styles.emptyMark
            }
          >
            <span>
              02
            </span>

            <div>
              <i />
              <i />
              <i />
            </div>
          </div>


          <div
            className={
              styles.emptyCopy
            }
          >
            <span>
              NENHUMA DISCIPLINA
            </span>

            <h3>
              Seu espaço acadêmico
              começa vazio.
            </h3>

            <p>
              Assim que sua matrícula
              e seu curso forem
              vinculados, suas
              disciplinas serão
              exibidas aqui.
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
          Disciplinas / NXS 02
        </span>
      </footer>
    </div>
  );
}