// frontend/src/api/memory.ts — методы памяти
// Назначение: list/add/delete

import { apiFetch } from "./http";

export type MemoryOut = {
  id: number;
  type: "profile" | "preference" | "shared_story";
  text: string;
  importance: number;
  created_at: string;
  updated_at: string | null;
};

export function memoryList(): Promise<MemoryOut[]> {
  return apiFetch<MemoryOut[]>("/api/v1/memory");
}

export function memoryAdd(type: MemoryOut["type"], text: string, importance = 3): Promise<MemoryOut> {
  return apiFetch<MemoryOut>("/api/v1/memory", {
    method: "POST",
    body: JSON.stringify({ type, text, importance }),
  });
}

export function memoryDelete(id: number): Promise<void> {
  return apiFetch<void>(`/api/v1/memory/${id}`, { method: "DELETE" });
}
