// frontend/src/api/auth.ts — методы авторизации
// Назначение: register/login/me

import { apiFetch, setToken } from "./http"; // (я добавил)

export type TokenOut = { access_token: string; token_type: string };
export type MeOut = { id: string; email: string };

export async function register(email: string, password: string): Promise<MeOut> {
  return apiFetch<MeOut>("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function login(email: string, password: string): Promise<TokenOut> {
  const token = await apiFetch<TokenOut>("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  setToken(token.access_token); // (я добавил)
  return token;
}

export async function me(): Promise<MeOut> {
  return apiFetch<MeOut>("/api/v1/auth/me");
}
