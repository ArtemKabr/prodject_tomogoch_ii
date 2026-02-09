// frontend/src/pages/ChatPage.tsx — чат: отправка, получение conversation_id, вывод сообщений

import { FormEvent, useEffect, useState } from "react";
import { chatHistory, chatSend, type HistoryItem } from "../api/chat"; // (я добавил)

type UiMsg = { role: string; text: string; created_at?: string };

const CONV_KEY = "conversation_id";

export default function ChatPage() {
  const [conversationId, setConversationId] = useState<number | null>(() => {
    const raw = localStorage.getItem(CONV_KEY);
    const n = raw ? Number(raw) : NaN;
    return Number.isFinite(n) ? n : null;
  });

  const [items, setItems] = useState<UiMsg[]>([]);
  const [message, setMessage] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadHistory(id: number) {
    const data = await chatHistory(id, 200, 0); // (я добавил)
    const mapped: UiMsg[] = (data.items || []).map((x: HistoryItem) => ({ // (я добавил)
      role: x.role,
      text: x.text,
      created_at: x.created_at,
    }));
    setItems(mapped);
  }

  useEffect(() => {
    setError(null);
    if (!conversationId) return;
    loadHistory(conversationId).catch(() => null);
  }, [conversationId]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    const text = message.trim();
    if (!text) return;

    setError(null);
    setLoading(true);

    setItems((prev) => [...prev, { role: "user", text }]);
    setMessage("");

    try {
      const out = await chatSend(text, conversationId ?? undefined); // (я добавил)
      setConversationId(out.conversation_id);
      localStorage.setItem(CONV_KEY, String(out.conversation_id));

      setItems((prev) => [...prev, { role: "assistant", text: out.assistant_message }]);
    } catch (err: any) {
      setError(err?.message ?? "Ошибка запроса"); // (я добавил)
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 900 }}>
      <h2>Chat</h2>

      <div style={{ marginBottom: 8 }}>
        conversation_id: <b>{conversationId ?? "null"}</b>{" "}
        <button
          onClick={() => {
            setConversationId(null);
            localStorage.removeItem(CONV_KEY);
            setItems([]);
          }}
        >
          reset
        </button>
      </div>

      <div style={{ border: "1px solid #ddd", padding: 12, minHeight: 260 }}>
        {items.length === 0 ? (
          <div>Пока пусто.</div>
        ) : (
          <div style={{ display: "grid", gap: 10 }}>
            {items.map((m, idx) => (
              <div key={idx}>
                <div style={{ fontSize: 12, opacity: 0.7 }}>{m.role}</div>
                <div style={{ whiteSpace: "pre-wrap" }}>{m.text}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      <form onSubmit={onSubmit} style={{ marginTop: 12, display: "flex", gap: 8 }}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Напиши сообщение..."
          style={{ flex: 1 }}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          send
        </button>
      </form>

      {error && <div style={{ marginTop: 8, color: "crimson" }}>{error}</div>}
    </div>
  );
}
