// frontend/src/pages/LoginPage.tsx — логин

import { FormEvent, useMemo, useState } from "react";
import { login } from "../api/auth";
import { Link, useLocation, useNavigate } from "react-router-dom";

export default function LoginPage() {
  const nav = useNavigate();
  const loc = useLocation();

  const from = useMemo(() => {
    const state = loc.state as any;
    return state?.from || "/pet";
  }, [loc.state]);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await login(email, password);
      nav(from, { replace: true });
    } catch (err: any) {
      setError(err?.message ?? "Ошибка запроса"); // (я добавил)
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 420 }}>
      <h2>Login</h2>

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
          {loading ? "..." : "Login"}
        </button>
      </form>

      {error && <div style={{ marginTop: 8, color: "crimson" }}>{error}</div>}

      <div style={{ marginTop: 12 }}>
        Нет аккаунта? <Link to="/register">register</Link>
      </div>
    </div>
  );
}
