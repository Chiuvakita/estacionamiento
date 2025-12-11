"use client";

import { useState } from "react";
import Link from "next/link";

export default function LoginPage() {
  const [rut, setRut] = useState("");
  const [clave, setClave] = useState("");
  const [messages, setMessages] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!rut || !clave) {
      setMessages("Debe completar ambos campos.");
      return;
    }

    console.log("Datos enviados:", { rut, clave });
    setMessages("Intentando iniciar sesión...");
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
        {/* Título */}
        <h1 className="text-center text-3xl font-bold mb-8 tracking-wide">
          Iniciar Sesión
        </h1>

        {/* Mensajes */}
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

        {/* Formulario */}
        <form onSubmit={handleSubmit} className="usuario-form flex flex-col gap-6">

          {/* RUT */}
          <div className="form-group">
            <label className="block mb-1 font-semibold text-sm">RUT:</label>
            <input
              type="number"
              placeholder="Ingrese su RUT sin puntos ni guión"
              value={rut}
              onChange={(e) => setRut(e.target.value)}
              className="form-control w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
            />
          </div>

          {/* CONTRASEÑA */}
          <div className="form-group">
            <label className="block mb-1 font-semibold text-sm">Contraseña:</label>
            <input
              type="password"
              placeholder="Ingrese su contraseña"
              value={clave}
              onChange={(e) => setClave(e.target.value)}
              className="form-control w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
            />
          </div>

          {/* Botón */}
          <button
            type="submit"
            className="button mt-3 w-full py-3 text-center font-semibold rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)] transition-transform hover:scale-[1.03]"
          >
            Ingresar
          </button>
        </form>

        {/* Registro */}
        <div className="mt-8 text-center">
          <p className="text-sm text-[var(--text-light)]">¿No tienes cuenta?</p>

          <Link
            href="/registro"
            className="button mt-3 inline-block px-6 py-3 bg-[var(--primary)] rounded-md hover:bg-[var(--primary-dark)] transition-transform hover:scale-[1.03)]"
          >
            Regístrate aquí
          </Link>
        </div>
      </div>
    </main>
  );
}
