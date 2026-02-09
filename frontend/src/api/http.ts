// frontend/src/api/http.ts — http клиент с JWT
// Назначение: единая обёртка fetch для backend

const API_BASE = import.meta.env.VITE_API_BASE ?? "";

const TOKEN_KEY = "token"; // (я добавил)
const CONV_KEY = "conversation_id"; // (я добавил)

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY); // (я добавил)
}

export function setToken(token: string): void { // (я добавил)
  localStorage.setItem(TOKEN_KEY, token); // (я добавил)
} // (я добавил)

export function clearToken(): void { // (я добавил)
  localStorage.removeItem(TOKEN_KEY); // (я добавил)
} // (я добавил)

function hardLogout(): void { // (я добавил)
  clearToken(); // (я добавил)
  localStorage.removeItem(CONV_KEY); // (я добавил)
  if (window.location.pathname !== "/login") { // (я добавил)
    window.location.href = "/login"; // (я добавил)
  } // (я добавил)
} // (я добавил)

async function readError(res: Response): Promise<string> { // (я добавил)
  const ct = res.headers.get("content-type") ?? ""; // (я добавил)
  const text = await res.text(); // (я добавил)
  if (!text) return `HTTP ${res.status}`; // (я добавил)

  if (ct.includes("application/json")) { // (я добавил)
    try { // (я добавил)
      const j = JSON.parse(text); // (я добавил)
      const detail = (j && (j.detail ?? j.message ?? j.error)) ?? j; // (я добавил)
      return typeof detail === "string" ? detail : JSON.stringify(detail); // (я добавил)
    } catch { // (я добавил)
      return text; // (я добавил)
    } // (я добавил)
  } // (я добавил)

  return text; // (я добавил)
} // (я добавил)

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = getToken();

  const baseHeaders: Record<string, string> = { // (я добавил)
    "Content-Type": "application/json", // (я добавил)
  }; // (я добавил)

  if (init.headers instanceof Headers) { // (я добавил)
    init.headers.forEach((v, k) => { // (я добавил)
      baseHeaders[k] = v; // (я добавил)
    }); // (я добавил)
  } else if (Array.isArray(init.headers)) { // (я добавил)
    for (const [k, v] of init.headers) { // (я добавил)
      baseHeaders[k] = v; // (я добавил)
    } // (я добавил)
  } else if (init.headers) { // (я добавил)
    Object.assign(baseHeaders, init.headers); // (я добавил)
  } // (я добавил)

  if (token) {
    baseHeaders["Authorization"] = `Bearer ${token}`; // (я добавил)
  }

  const res = await fetch(`${API_BASE}${path}`, { ...init, headers: baseHeaders }); // (я добавил)

  if (res.status === 401) {
    hardLogout();
    throw new Error("Unauthorized");
  }

  if (!res.ok) {
    throw new Error(await readError(res));
  }

  if (res.status === 204) {
    return undefined as T;
  }

  const text = await res.text();
  if (!text) return undefined as T;

  return JSON.parse(text) as T;
}
