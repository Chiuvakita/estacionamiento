"use client";

import { useState } from "react";
import Link from "next/link";

export default function RegistroPage() {
  const [form, setForm] = useState({
    rut: "",
    nombre: "",
    apellidoPaterno: "",
    apellidoMaterno: "",
    numeroTelefono: "",
    discapacidad: false,
    clave: "",
    confirmarClave: "",
  });

  const [messages, setMessages] = useState<string | null>(null);

  const handleChange = (e: any) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (form.clave !== form.confirmarClave) {
      setMessages("Las contraseñas no coinciden.");
      return;
    }

    console.log("Datos de registro enviados:", form);
    setMessages("Procesando registro...");
  };

  return (
    <main className="min-h-screen flex items-center justify-center p-5 bg-[var(--bg)] text-[var(--text)]">
      <div
        className="w-full max-w-lg p-8 card"
        style={{
          background: "var(--bg-card)",
          borderRadius: "var(--radius)",
          boxShadow: "var(--shadow)",
        }}
      >
        <h1 className="text-center text-3xl font-bold mb-8">
          Registro de Cliente
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

        {/* FORMULARIO */}
        <form className="usuario-form flex flex-col gap-6" onSubmit={handleSubmit}>

          {/* RUT */}
          <div className="form-group">
            <label className="font-semibold">RUT:</label>
            <input
              type="number"
              name="rut"
              value={form.rut}
              onChange={handleChange}
              placeholder="Ingrese su RUT"
              className="form-control w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
            />
          </div>

          {/* Nombre */}
          <div className="form-group">
            <label className="font-semibold">Nombre:</label>
            <input
              type="text"
              name="nombre"
              value={form.nombre}
              onChange={handleChange}
              placeholder="Ej: Juan"
              className="form-control w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
            />
          </div>

          {/* Apellido paterno */}
          <div className="form-group">
            <label className="font-semibold">Apellido Paterno:</label>
            <input
              type="text"
              name="apellidoPaterno"
              value={form.apellidoPaterno}
              onChange={handleChange}
              placeholder="Ej: López"
              className="form-control w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
            />
          </div>

          {/* Apellido materno */}
          <div className="form-group">
            <label className="font-semibold">Apellido Materno:</label>
            <input
              type="text"
              name="apellidoMaterno"
              value={form.apellidoMaterno}
              onChange={handleChange}
              placeholder="Ej: Pérez"
              className="form-control w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
            />
          </div>

          {/* Teléfono */}
          <div className="form-group">
            <label className="font-semibold">Número de Teléfono:</label>
            <input
              type="number"
              name="numeroTelefono"
              value={form.numeroTelefono}
              onChange={handleChange}
              placeholder="Ej: 987654321"
              className="form-control w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
            />
          </div>

          {/* Discapacidad */}
          <div className="checkbox-group flex items-center gap-3">
            <input
              type="checkbox"
              name="discapacidad"
              checked={form.discapacidad}
              onChange={handleChange}
              className="h-5 w-5"
            />
            <label className="font-semibold">¿Posee discapacidad?</label>
          </div>

          {/* Contraseña */}
          <div className="form-group">
            <label className="font-semibold">Contraseña:</label>
            <input
              type="password"
              name="clave"
              value={form.clave}
              onChange={handleChange}
              placeholder="Ingrese su contraseña"
              className="form-control w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
            />
          </div>

          {/* Confirmar contraseña */}
          <div className="form-group">
            <label className="font-semibold">Confirmar Contraseña:</label>
            <input
              type="password"
              name="confirmarClave"
              value={form.confirmarClave}
              onChange={handleChange}
              placeholder="Repita su contraseña"
              className="form-control w-full px-4 py-2 rounded-md bg-[var(--bg-card)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
            />
          </div>

          {/* Botones */}
          <div className="form-actions flex justify-center gap-4 mt-4">
            <button
              type="submit"
              className="button px-6 py-3 text-white font-semibold rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)] transition-transform hover:scale-[1.03]"
            >
              Registrarse
            </button>

            <Link
              href="/login"
              className="button px-6 py-3 text-white font-semibold rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)] transition-transform hover:scale-[1.03]"
            >
              Ya tengo cuenta
            </Link>
          </div>
        </form>
      </div>
    </main>
  );
}
