"use client";

import {
  useEffect,
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

export default function Dashboard() {
  const router = useRouter();

  const [user, setUser] =
    useState<NexusUser | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [loggingOut, setLoggingOut] =
    useState(false);

  useEffect(() => {
    let active = true;

    async function loadUser() {
      try {
        const response = await apiFetch(
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

  async function handleLogout() {
    setLoggingOut(true);

    await logout();

    router.replace("/");
    router.refresh();
  }

  if (loading) {
    return (
      <main className="dashboard-loading">
        <span>NXS</span>
        <p>Carregando ambiente acadêmico...</p>
      </main>
    );
  }

  if (!user) {
    return null;
  }

  const name =
    user.first_name ||
    user.full_name ||
    user.email;

  return (
    <main className="dashboard-test">
      <header>
        <div>
          <span className="dashboard-eyebrow">
            NEXUS ACADEMY / SESSÃO
          </span>

          <h1>
            Olá, {name}.
          </h1>

          <p>
            Sua sessão está autenticada e
            protegida pelo Nexus.
          </p>
        </div>

        <button
          type="button"
          onClick={handleLogout}
          disabled={loggingOut}
        >
          {loggingOut
            ? "Saindo..."
            : "Encerrar sessão"}
        </button>
      </header>

      <section>
        <span>PERFIL ATUAL</span>

        <strong>{user.role}</strong>

        <p>{user.email}</p>
      </section>
    </main>
  );
}