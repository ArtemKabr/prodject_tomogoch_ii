// frontend/src/api/pet.ts — методы питомца
// Назначение: start/get/revive

import { apiFetch } from "./http";

export type PetOut = {
  id: number;
  age_stage: string;
  health: number;
  energy: number;
  mood: number;
  intellect: number;
  bond: number;
  is_alive: boolean;
  last_active_at: string;
  created_at: string;
  died_at: string | null;
};

export function petStart(): Promise<PetOut> {
  return apiFetch<PetOut>("/api/v1/pet/start", { method: "POST" });
}

export function petGet(): Promise<PetOut> {
  return apiFetch<PetOut>("/api/v1/pet");
}

export function petRevive(): Promise<PetOut> {
  return apiFetch<PetOut>("/api/v1/pet/revive", { method: "POST" });
}
