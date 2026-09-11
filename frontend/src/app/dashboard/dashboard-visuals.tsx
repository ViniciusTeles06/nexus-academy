import styles from "./dashboard-visuals.module.css";


type DashboardVisualProps = {
  type:
    | "overview"
    | "subjects"
    | "grades"
    | "attendance"
    | "agenda";
};


function OverviewVisual() {
  return (
    <div
      className={`${styles.visual} ${styles.overview}`}
      aria-hidden="true"
    >
      <span
        className={
          styles.overviewOrbitOuter
        }
      />

      <span
        className={
          styles.overviewOrbitMiddle
        }
      />

      <span
        className={
          styles.overviewOrbitInner
        }
      />

      <div
        className={
          styles.overviewCore
        }
      >
        <span>N</span>
      </div>

      <span
        className={`${styles.orbitPoint} ${styles.orbitPointOne}`}
      />

      <span
        className={`${styles.orbitPoint} ${styles.orbitPointTwo}`}
      />

      <div
        className={`${styles.glassLabel} ${styles.overviewLabel}`}
      >
        <span>NXS</span>

        <strong>
          Ambiente conectado
        </strong>
      </div>
    </div>
  );
}


function SubjectsVisual() {
  return (
    <div
      className={`${styles.visual} ${styles.subjects}`}
      aria-hidden="true"
    >
      <div
        className={`${styles.subjectSheet} ${styles.subjectSheetBack}`}
      >
        <span>03</span>
      </div>

      <div
        className={`${styles.subjectSheet} ${styles.subjectSheetMiddle}`}
      >
        <span>02</span>
      </div>

      <div
        className={`${styles.subjectSheet} ${styles.subjectSheetFront}`}
      >
        <header>
          <span>
            NXS / DISCIPLINA
          </span>

          <i />
        </header>

        <strong>
          CC
        </strong>

        <div
          className={
            styles.subjectLines
          }
        >
          <span />
          <span />
          <span />
        </div>
      </div>

      <span
        className={`${styles.subjectDot} ${styles.subjectDotOne}`}
      />

      <span
        className={`${styles.subjectDot} ${styles.subjectDotTwo}`}
      />

      <div
        className={`${styles.glassLabel} ${styles.subjectLabel}`}
      >
        <span>SEMESTRE</span>

        <strong>
          Tudo organizado
        </strong>
      </div>
    </div>
  );
}


function GradesVisual() {
  return (
    <div
      className={`${styles.visual} ${styles.grades}`}
      aria-hidden="true"
    >
      <div
        className={
          styles.gradeAxis
        }
      >
        <span />
        <span />
        <span />
        <span />
      </div>

      <svg
        className={
          styles.gradeGraph
        }
        viewBox="0 0 500 340"
        fill="none"
      >
        <path
          className={
            styles.gradeGraphGhost
          }
          d="M20 268C90 262 105 220 160 228C220 238 238 160 297 180C348 198 373 88 480 73"
        />

        <path
          className={
            styles.gradeGraphActive
          }
          d="M20 268C90 262 105 220 160 228C220 238 238 160 297 180C348 198 373 88 480 73"
        />
      </svg>

      <span
        className={`${styles.gradePoint} ${styles.gradePointOne}`}
      />

      <span
        className={`${styles.gradePoint} ${styles.gradePointTwo}`}
      />

      <span
        className={`${styles.gradePoint} ${styles.gradePointThree}`}
      />

      <div
        className={
          styles.gradeScore
        }
      >
        <span>
          MÉDIA
        </span>

        <strong>
          —
        </strong>
      </div>

      <div
        className={`${styles.glassLabel} ${styles.gradeLabel}`}
      >
        <span>DESEMPENHO</span>

        <strong>
          Evolução clara
        </strong>
      </div>
    </div>
  );
}


function AttendanceVisual() {
  return (
    <div
      className={`${styles.visual} ${styles.attendance}`}
      aria-hidden="true"
    >
      <svg
        className={
          styles.attendanceRing
        }
        viewBox="0 0 420 420"
      >
        <circle
          className={
            styles.attendanceTrack
          }
          cx="210"
          cy="210"
          r="145"
        />

        <circle
          className={
            styles.attendanceProgress
          }
          cx="210"
          cy="210"
          r="145"
        />
      </svg>

      <span
        className={
          styles.attendanceRingInner
        }
      />

      <div
        className={
          styles.attendanceCore
        }
      >
        <strong>
          %
        </strong>

        <span>
          PRESENÇA
        </span>
      </div>

      <div
        className={
          styles.attendanceTicks
        }
      >
        {Array.from({
          length: 12,
        }).map((_, index) => (
          <i
            key={index}
            style={{
              transform:
                `rotate(${index * 30}deg)`,
            }}
          />
        ))}
      </div>

      <div
        className={`${styles.glassLabel} ${styles.attendanceLabel}`}
      >
        <span>FREQUÊNCIA</span>

        <strong>
          Sempre visível
        </strong>
      </div>
    </div>
  );
}


function AgendaVisual() {
  return (
    <div
      className={`${styles.visual} ${styles.agenda}`}
      aria-hidden="true"
    >
      <div
        className={
          styles.calendar
        }
      >
        <header>
          <span>
            NXS / AGENDA
          </span>

          <div>
            <i />
            <i />
          </div>
        </header>

        <div
          className={
            styles.calendarWeek
          }
        >
          <span>SEG</span>
          <span>TER</span>
          <span>QUA</span>
          <span>QUI</span>
          <span>SEX</span>
        </div>

        <div
          className={
            styles.calendarGrid
          }
        >
          {Array.from({
            length: 15,
          }).map((_, index) => (
            <span
              key={index}
              className={
                index === 7
                  ? styles.calendarActive
                  : ""
              }
            >
              {index + 1}
            </span>
          ))}
        </div>
      </div>

      <span
        className={
          styles.timeline
        }
      />

      <span
        className={`${styles.timelinePoint} ${styles.timelinePointOne}`}
      />

      <span
        className={`${styles.timelinePoint} ${styles.timelinePointTwo}`}
      />

      <div
        className={`${styles.glassLabel} ${styles.agendaLabel}`}
      >
        <span>PRÓXIMO</span>

        <strong>
          Tudo no tempo certo
        </strong>
      </div>
    </div>
  );
}


export default function DashboardVisual({
  type,
}: DashboardVisualProps) {
  if (type === "subjects") {
    return <SubjectsVisual />;
  }

  if (type === "grades") {
    return <GradesVisual />;
  }

  if (
    type === "attendance"
  ) {
    return <AttendanceVisual />;
  }

  if (type === "agenda") {
    return <AgendaVisual />;
  }

  return <OverviewVisual />;
}