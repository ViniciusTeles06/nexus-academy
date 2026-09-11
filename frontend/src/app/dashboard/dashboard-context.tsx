"use client";

import {
  createContext,
  useContext,
  type ReactNode,
} from "react";

import type {
  Membership,
} from "@/lib/api";


export type DashboardUser = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  avatar?: string | null;
  role:
    | "STUDENT"
    | "TEACHER"
    | "ADMIN";
  is_email_verified: boolean;
};


type DashboardContextValue = {
  user: DashboardUser;
  membership: Membership;
  institutionName: string;
  roleLabel: string;
};


const DashboardContext =
  createContext<
    DashboardContextValue | null
  >(null);


type DashboardProviderProps = {
  children: ReactNode;
  value: DashboardContextValue;
};


export function DashboardProvider({
  children,
  value,
}: DashboardProviderProps) {
  return (
    <DashboardContext.Provider
      value={value}
    >
      {children}
    </DashboardContext.Provider>
  );
}


export function useDashboard() {
  const context =
    useContext(
      DashboardContext,
    );

  if (!context) {
    throw new Error(
      "useDashboard precisa estar dentro de DashboardProvider.",
    );
  }

  return context;
}