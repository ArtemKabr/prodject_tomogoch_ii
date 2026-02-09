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

export type HistoryItem = { // (я добавил)
  role: "user" | "assistant"; // (я добавил)
  text: string; // (я добавил)
  created_at: string; // (я добавил)
}; // (я добавил)

export function chatSend(message: string, conversation_id?: number): Promise<ChatOut> {
  return apiFetch<ChatOut>("/api/v1/chat", {
    method: "POST",
    body: JSON.stringify({ message, conversation_id }),
  });
}

export function chatHistory( // (я добавил)
  conversation_id: number, // (я добавил)
  limit = 50, // (я добавил)
  offset = 0, // (я добавил)
): Promise<{ items: HistoryItem[] }> { // (я добавил)
  const qs = new URLSearchParams({
    conversation_id: String(conversation_id),
    limit: String(limit),
    offset: String(offset),
  });
  return apiFetch<{ items: HistoryItem[] }>(`/api/v1/chat/history?${qs.toString()}`); // (я добавил)
}
