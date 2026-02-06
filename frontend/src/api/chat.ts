// frontend/src/api/chat.ts — методы чата
// Назначение: отправка сообщений и история

import { apiFetch } from "./http";
import type { PetOut } from "./pet";

export type ChatOut = {
  assistant_message: string;
  stage: string;
  conversation_id: number;
  pet_state: PetOut;
};

export function chatSend(message: string, conversation_id?: number): Promise<ChatOut> {
  return apiFetch<ChatOut>("/api/v1/chat", {
    method: "POST",
    body: JSON.stringify({ message, conversation_id }),
  });
}

export function chatHistory(conversation_id: number, limit = 50, offset = 0): Promise<{ items: any[] }> {
  const qs = new URLSearchParams({
    conversation_id: String(conversation_id),
    limit: String(limit),
    offset: String(offset),
  });
  return apiFetch<{ items: any[] }>(`/api/v1/chat/history?${qs.toString()}`);
}
