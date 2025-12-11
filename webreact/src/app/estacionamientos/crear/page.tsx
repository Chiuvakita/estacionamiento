"use client";

import NavbarAdmin from "@/components/NavbarAdmin";
import Link from "next/link";
import { useState } from "react";

export default function CrearEstacionamientoPage() {
  const [estado, setEstado] = useState("L");
  const [tipo, setTipo] = useState("Auto");
  const [patente, setPatente] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (patente.trim() === "") {
      alert("Debe ingresar una patente o dejar '-' si no corresponde.");
      return;
    }

    alert(`Creando estacionamiento:
    Estado: ${estado}
    Tipo: ${tipo}
    Patente: ${patente} (simulación)`);
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-xl mx-auto p-6 mt-6">
        <h1 className="text-3xl font-bold text-center mb-6">
          Crear Estacionamiento
        </h1>

        {/* CARD */}
        <div
          className="p-8 rounded-[var(--radius)] shadow-lg"
          style={{ background: "var(--bg-card)" }}
        >
          <form onSubmit={handleSubmit} className="space-y-6">

            {/* ESTADO */}
            <div>
              <label className="block text-sm font-semibold mb-2">Estado</label>
              <select
                value={estado}
                onChange={(e) => setEstado(e.target.value)}
                className="
                  w-full px-4 py-3 rounded-md
                  bg-[var(--bg-alt)]
                  border border-[var(--bg-alt)]
                  focus:border-[var(--primary)]
                  focus:ring-2 focus:ring-[var(--primary)]
                  transition
                "
              >
                <option value="L">Libre</option>
                <option value="O">Ocupado</option>
              </select>
            </div>

            {/* TIPO */}
            <div>
              <label className="block text-sm font-semibold mb-2">Tipo</label>
              <select
                value={tipo}
                onChange={(e) => setTipo(e.target.value)}
                className="
                  w-full px-4 py-3 rounded-md
                  bg-[var(--bg-alt)]
                  border border-[var(--bg-alt)]
                  focus:border-[var(--primary)]
                  focus:ring-2 focus:ring-[var(--primary)]
                  transition
                "
              >
                <option value="Auto">Auto</option>
                <option value="Moto">Moto</option>
              </select>
            </div>

            {/* PATENTE */}
            <div>
              <label className="block text-sm font-semibold mb-2">Patente</label>
              <input
                type="text"
                value={patente}
                onChange={(e) => setPatente(e.target.value.toUpperCase())}
                placeholder="Ej: ABCD12"
                className="
                  w-full px-4 py-3 rounded-md
                  bg-[var(--bg-alt)]
                  border border-[var(--bg-alt)]
                  focus:border-[var(--primary)]
                  focus:ring-2 focus:ring-[var(--primary)]
                  transition uppercase
                "
              />
            </div>

            {/* BOTÓN CREAR */}
            <button
              type="submit"
              className="
                w-full py-3 rounded-md text-center
                button bg-[var(--primary)]
                hover:bg-[var(--primary-dark)]
                font-semibold
              "
            >
              Crear Estacionamiento
            </button>

            {/* BOTÓN CANCELAR */}
            <Link
              href="/estacionamientos/listar"
              className="
                w-full block text-center py-3 mt-2 rounded-md
                button-danger font-semibold
              "
            >
              Cancelar
            </Link>
          </form>
        </div>
      </main>
    </div>
  );
}
