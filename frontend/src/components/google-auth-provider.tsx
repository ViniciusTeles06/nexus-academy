"use client";

import { GoogleOAuthProvider } from "@react-oauth/google";

type GoogleAuthProviderProps = {
  children: React.ReactNode;
};

export default function GoogleAuthProvider({
  children,
}: GoogleAuthProviderProps) {
  const clientId =
    process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID ?? "";

  return (
    <GoogleOAuthProvider clientId={clientId}>
      {children}
    </GoogleOAuthProvider>
  );
}