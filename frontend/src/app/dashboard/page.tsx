"use client";

import {
  useEffect,
  useSyncExternalStore,
} from "react";
import { useRouter } from "next/navigation";

type NexusUser = {
  email: string;
  first_name: string;
  full_name: string;
  role: string;
};

function subscribe() {
  return () => {};
}

function getUserSnapshot() {
  return sessionStorage.getItem("nexus_user");
}

function getAccessSnapshot() {
  return sessionStorage.getItem("nexus_access");
}

function getServerSnapshot() {
  return null;
}

export default function Dashboard() {
  const router = useRouter();

  const storedUser = useSyncExternalStore(
    subscribe,
    getUserSnapshot,
    getServerSnapshot,
  );

  const access = useSyncExternalStore(
    subscribe,
    getAccessSnapshot,
    getServerSnapshot,
  );

  let user: NexusUser | null = null;

  if (storedUser) {
    try {
      user = JSON.parse(storedUser) as NexusUser;
    } catch {
      user = null;
    }
  }

  useEffect(() => {
    if (!access || !storedUser) {
      router.replace("/");
    }
  }, [access, storedUser, router]);

  if (!access || !user) {
    return null;
  }

  const name =
    user.first_name ||
    user.full_name ||
    user.email;

  return (
    <main
      style={{
        minHeight: "100vh",
        padding: "48px",
        background: "#f2efe7",
        color: "#151a22",
      }}
    >
      <p
        style={{
          fontSize: "10px",
          letterSpacing: ".16em",
          fontWeight: 800,
          color: "#68717c",
        }}
      >
        NEXUS ACADEMY / SESSÃO
      </p>

      <h1
        style={{
          marginTop: "60px",
          fontFamily:
            "var(--font-serif), serif",
          fontSize: "64px",
          fontWeight: 400,
        }}
      >
        Olá, {name}.
      </h1>

      <p>
        Seu login foi realizado com sucesso.
      </p>

      <p>
        Perfil: <strong>{user.role}</strong>
      </p>
    </main>
  );
}