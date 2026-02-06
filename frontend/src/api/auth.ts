// frontend/src/api/auth.ts — методы авторизации
// Назначение: register/login/me

import { apiFetch } from "./http";

export type TokenOut = { access_token: string; token_type: string };
export type MeOut = { id: string; email: string };

export async function register(email: string, password: string): Promise<MeOut> {
  return apiFetch<MeOut>("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function login(email: string, password: string): Promise<TokenOut> {
  return apiFetch<TokenOut>("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function me(): Promise<MeOut> {
  return apiFetch<MeOut>("/api/v1/auth/me");
}
