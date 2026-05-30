import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Dashboard from "@/pages/Dashboard";
import FieldDetail from "@/pages/FieldDetail";
import Recommendations from "@/pages/Recommendations";
import Login from "@/pages/Login";
import { useAppSelector } from "@/store";

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const token = useAppSelector((s) => s.field.token);
  return token ? <>{children}</> : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <div className="app">
      <Navbar />
      <main className="main-content">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/fields/:fieldId"
            element={
              <PrivateRoute>
                <FieldDetail />
              </PrivateRoute>
            }
          />
          <Route
            path="/fields/:fieldId/recommendations"
            element={
              <PrivateRoute>
                <Recommendations />
              </PrivateRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
