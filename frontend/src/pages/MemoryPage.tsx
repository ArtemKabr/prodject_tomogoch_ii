// frontend/src/pages/MemoryPage.tsx — read-only список памяти

import { useEffect, useState } from "react";
import { memoryList, type MemoryOut } from "../api/memory"; // (я добавил)

export default function MemoryPage() {
  const [items, setItems] = useState<MemoryOut[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setError(null);
    setLoading(true);
    try {
      const data = await memoryList(); // (я добавил)
      setItems(data);
    } catch (err: any) {
      setError(err?.message ?? "Ошибка запроса"); // (я добавил)
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div style={{ maxWidth: 900 }}>
      <h2>Memory</h2>

      <button onClick={load} disabled={loading}>
        refresh
      </button>

      {error && <div style={{ marginTop: 8, color: "crimson" }}>{error}</div>}

      <div style={{ marginTop: 12, display: "grid", gap: 10 }}>
        {items.length === 0 ? (
          <div>Память пустая.</div>
        ) : (
          items.map((m) => (
            <div key={m.id} style={{ border: "1px solid #ddd", padding: 10 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <b>
                  #{m.id} {m.type}
                </b>
                <span>importance: {m.importance}</span>
              </div>
              <div style={{ marginTop: 6, whiteSpace: "pre-wrap" }}>{m.text}</div>
              <div style={{ marginTop: 6, fontSize: 12, opacity: 0.7 }}>
                created_at: {m.created_at}
                {m.updated_at ? ` | updated_at: ${m.updated_at}` : ""}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
