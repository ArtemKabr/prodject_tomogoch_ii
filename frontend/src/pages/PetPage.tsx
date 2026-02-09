// frontend/src/pages/PetPage.tsx — состояние питомца + start/revive

import { useEffect, useState } from "react";
import { petGet, petRevive, petStart, type PetOut } from "../api/pet"; // (я добавил)

export default function PetPage() {
  const [pet, setPet] = useState<PetOut | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setError(null);
    setLoading(true);
    try {
      const data = await petGet(); // (я добавил)
      setPet(data);
    } catch (err: any) {
      // backend на отсутствие питомца может отдавать 404 "Pet not found"
      if (String(err?.message ?? "").includes("404")) setPet(null); // (я добавил)
      else setError(err?.message ?? "Ошибка запроса"); // (я добавил)
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function onStart() {
    setError(null);
    setLoading(true);
    try {
      const data = await petStart(); // (я добавил)
      setPet(data);
    } catch (err: any) {
      setError(err?.message ?? "Ошибка запроса"); // (я добавил)
    } finally {
      setLoading(false);
    }
  }

  async function onRevive() {
    setError(null);
    setLoading(true);
    try {
      const data = await petRevive(); // (я добавил)
      setPet(data);
    } catch (err: any) {
      setError(err?.message ?? "Ошибка запроса"); // (я добавил)
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 700 }}>
      <h2>Pet</h2>

      <button onClick={load} disabled={loading}>
        refresh
      </button>

      {!pet ? (
        <div style={{ marginTop: 12 }}>
          <div>Питомца нет.</div>
          <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
            <button onClick={onStart} disabled={loading}>
              start
            </button>
            <button onClick={onRevive} disabled={loading}>
              revive
            </button>
          </div>
        </div>
      ) : (
        <div style={{ marginTop: 12, display: "grid", gap: 6 }}>
          <div>id: {pet.id}</div>
          <div>age_stage: {pet.age_stage}</div>
          <div>is_alive: {String(pet.is_alive)}</div>
          <div>health: {pet.health}</div>
          <div>energy: {pet.energy}</div>
          <div>mood: {pet.mood}</div>
          <div>intellect: {pet.intellect}</div>
          <div>bond: {pet.bond}</div>
          <div>last_active_at: {pet.last_active_at}</div>
        </div>
      )}

      {error && <div style={{ marginTop: 8, color: "crimson" }}>{error}</div>}
    </div>
  );
}
