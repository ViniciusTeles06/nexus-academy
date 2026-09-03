import type { Metadata } from "next";
import {
  DM_Serif_Display,
  Manrope,
} from "next/font/google";

import GoogleAuthProvider from "@/components/google-auth-provider";

import "./globals.css";

const serif = DM_Serif_Display({
  variable: "--font-serif",
  subsets: ["latin"],
  weight: "400",
});

const sans = Manrope({
  variable: "--font-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Nexus Academy",
  description: "Ambiente acadêmico Nexus Academy",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body
        className={`${serif.variable} ${sans.variable}`}
      >
        <GoogleAuthProvider>
          {children}
        </GoogleAuthProvider>
      </body>
    </html>
  );
}