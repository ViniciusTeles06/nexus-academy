"use client";

import DashboardVisual from "./dashboard-visuals";

import {
  useDashboard,
} from "./dashboard-context";

import styles from "./overview.module.css";


function getGreeting() {
  const hour =
    new Date().getHours();

  if (hour < 12) {
    return "Bom dia";
  }

  if (hour < 18) {
    return "Boa tarde";
  }

  return "Boa noite";
}


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


export default function DashboardOverviewPage() {
  const {
    user,
    institutionName,
  } =
    useDashboard();


  const date =
    getCurrentDate();


  const name =
    user.first_name ||
    user.full_name ||
    user.email.split("@")[0];


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
              /01
            </span>

            <i />

            <span>
              VISÃO GERAL
            </span>
          </div>


          <h1>
            {getGreeting()},
            <br />

            <span>
              {name}.
            </span>
          </h1>


          <p
            className={
              styles.lead
            }
          >
            Seu ambiente acadêmico
            começa aqui.
            Informações essenciais,
            organizadas sem ruído.
          </p>


          <div
            className={
              styles.heroMeta
            }
          >
            <div>
              <span>
                INSTITUIÇÃO
              </span>

              <strong>
                {
                  institutionName
                }
              </strong>
            </div>

            <div>
              <span>
                STATUS
              </span>

              <strong>
                Ambiente ativo
              </strong>
            </div>
          </div>
        </div>


        <div
          className={
            styles.heroVisual
          }
        >
          <DashboardVisual
            type="overview"
          />
        </div>
      </section>


      <section
        className={
          styles.infoGrid
        }
      >
        <article
          className={
            styles.todayCard
          }
        >
          <div
            className={
              styles.cardTop
            }
          >
            <span>
              HOJE
            </span>

            <span>
              NXS / 01
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
              styles.statusRow
            }
          >
            <i />

            <div>
              <strong>
                Agenda disponível
              </strong>

              <p>
                Nenhum compromisso
                acadêmico sincronizado
                ainda.
              </p>
            </div>
          </div>
        </article>


        <article
          className={
            styles.summaryCard
          }
        >
          <span
            className={
              styles.summaryIndex
            }
          >
            01
          </span>

          <span
            className={
              styles.summaryLabel
            }
          >
            CURSO
          </span>

          <strong>
            Ainda não vinculado
          </strong>

          <p>
            Seu perfil acadêmico
            será exibido assim que
            a matrícula for
            associada.
          </p>
        </article>


        <article
          className={
            styles.summaryCard
          }
        >
          <span
            className={
              styles.summaryIndex
            }
          >
            02
          </span>

          <span
            className={
              styles.summaryLabel
            }
          >
            PERÍODO
          </span>

          <strong>
            —
          </strong>

          <p>
            O período atual será
            exibido após o vínculo
            acadêmico.
          </p>
        </article>


        <article
          className={
            styles.summaryCard
          }
        >
          <span
            className={
              styles.summaryIndex
            }
          >
            03
          </span>

          <span
            className={
              styles.summaryLabel
            }
          >
            MATRÍCULA
          </span>

          <strong>
            —
          </strong>

          <p>
            Nenhuma matrícula
            acadêmica vinculada
            ainda.
          </p>
        </article>
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
          Ambiente acadêmico digital
        </span>
      </footer>
    </div>
  );
}