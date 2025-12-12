"use client";

import { useState } from "react";
import Link from "next/link";
import { login } from "@/services/auth";
import { useRouter } from "next/navigation";
import { AxiosError } from "axios";

export default function LoginPage() {
  const [rut, setRut] = useState("");
  const [clave, setClave] = useState("");
  const [messages, setMessages] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessages(null);

    if (!rut || !clave) {
      setMessages("Debe completar ambos campos.");
      return;
    }

    try {
      setMessages("Iniciando sesión...");

      const data = await login(rut, clave);

      if (data.token && data.usuario) {
        // 🔐 guardar sesión
        localStorage.setItem("token", data.token);
        localStorage.setItem("usuario", JSON.stringify(data.usuario));

        setMessages("Inicio de sesión exitoso");

        // 🔁 redirección por rol
        if (data.usuario.rol === "Administrador") {
          router.push("/admin");
        } else {
          router.push("/cliente");
        }
      } else {
        setMessages("Credenciales inválidas.");
      }
    } catch (error) {
      const err = error as AxiosError<any>;
      setMessages(
        err.response?.data?.detail || "Error al iniciar sesión"
      );
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center p-5 bg-[var(--bg)] text-[var(--text)]">
      <div
        className="w-full max-w-md p-8 card"
        style={{
          background: "var(--bg-card)",
          borderRadius: "var(--radius)",
          boxShadow: "var(--shadow)",
        }}
      >
        <h1 className="text-center text-3xl font-bold mb-8 tracking-wide">
          Iniciar Sesión
        </h1>

        {messages && (
          <div
            className="mb-5 alert"
            style={{
              backgroundColor: "rgba(255, 93, 108, 0.12)",
              border: "1px solid var(--danger)",
              color: "var(--danger)",
              borderRadius: "var(--radius)",
              padding: "12px 16px",
            }}
          >
            {messages}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
          <div>
            <label className="block mb-1 font-semibold text-sm">RUT:</label>
            <input
              type="number"
              value={rut}
              onChange={(e) => setRut(e.target.value)}
              className="w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)]"
            />
          </div>

          <div>
            <label className="block mb-1 font-semibold text-sm">Contraseña:</label>
            <input
              type="password"
              value={clave}
              onChange={(e) => setClave(e.target.value)}
              className="w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)]"
            />
          </div>

          <button
            type="submit"
            className="button w-full py-3 bg-[var(--primary)] hover:bg-[var(--primary-dark)]"
          >
            Ingresar
          </button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-sm text-[var(--text-light)]">
            ¿No tienes cuenta?
          </p>

          <Link
            href="/registro"
            className="button mt-3 inline-block px-6 py-3 bg-[var(--primary)]"
          >
            Regístrate aquí
          </Link>
        </div>
      </div>
    </main>
  );
}
