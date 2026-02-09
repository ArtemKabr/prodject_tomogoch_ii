// frontend/src/pages/RegisterPage.tsx — регистрация

import { FormEvent, useState } from "react";
import { register } from "../api/auth";
import { Link, useNavigate } from "react-router-dom";

export default function RegisterPage() {
  const nav = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await register(email, password);
      nav("/login", { replace: true });
    } catch (err: any) {
      setError(err?.message ?? "Ошибка запроса"); // (я добавил)
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 420 }}>
      <h2>Register</h2>

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 8 }}>
        <label>
          Email
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
        </label>

        <label>
          Password
          <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
        </label>

        <button disabled={loading} type="submit">
          {loading ? "..." : "Create"}
        </button>
      </form>

      {error && <div style={{ marginTop: 8, color: "crimson" }}>{error}</div>}

      <div style={{ marginTop: 12 }}>
        Уже есть аккаунт? <Link to="/login">login</Link>
      </div>
    </div>
  );
}
