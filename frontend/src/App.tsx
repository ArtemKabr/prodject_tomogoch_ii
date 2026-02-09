// frontend/src/App.tsx — роутинг, guard по токену, минимальная навигация

import { Link, Navigate, Route, Routes, useLocation } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import PetPage from "./pages/PetPage";
import ChatPage from "./pages/ChatPage";
import MemoryPage from "./pages/MemoryPage";
import { clearToken, getToken } from "./api/http";

const CONV_KEY = "conversation_id"; // (я добавил)

function RequireAuth({ children }: { children: JSX.Element }) {
  const token = getToken();
  const location = useLocation();

  if (!token) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }
  return children;
}

function Nav() {
  const token = getToken();

  return (
    <div style={{ display: "flex", gap: 12, padding: 12, borderBottom: "1px solid #ddd" }}>
      <Link to="/pet">pet</Link>
      <Link to="/chat">chat</Link>
      <Link to="/memory">memory</Link>

      <div style={{ marginLeft: "auto" }}>
        {!token ? (
          <>
            <Link to="/login" style={{ marginRight: 12 }}>
              login
            </Link>
            <Link to="/register">register</Link>
          </>
        ) : (
          <button
            onClick={() => {
              clearToken();
              localStorage.removeItem(CONV_KEY); // (я добавил)
              window.location.href = "/login";
            }}
          >
            logout
          </button>
        )}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <div>
      <Nav />
      <div style={{ padding: 12 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/pet" replace />} />

          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route
            path="/pet"
            element={
              <RequireAuth>
                <PetPage />
              </RequireAuth>
            }
          />
          <Route
            path="/chat"
            element={
              <RequireAuth>
                <ChatPage />
              </RequireAuth>
            }
          />
          <Route
            path="/memory"
            element={
              <RequireAuth>
                <MemoryPage />
              </RequireAuth>
            }
          />

          <Route path="*" element={<div>not found</div>} />
        </Routes>
      </div>
    </div>
  );
}
