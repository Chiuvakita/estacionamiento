"use client";

import NavbarAdmin from "@/components/NavbarAdmin";
import { useState } from "react";
import Link from "next/link";

export default function CrearMasivoPage() {
  const [cantidad, setCantidad] = useState("");
  const [tipo, setTipo] = useState("Auto");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!cantidad || isNaN(Number(cantidad)) || Number(cantidad) <= 0) {
      alert("La cantidad debe ser un número válido.");
      return;
    }

    alert(`Creando ${cantidad} estacionamientos tipo ${tipo} (simulación)`);
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-xl mx-auto p-6 mt-6">
        <h1 className="text-3xl font-bold text-center mb-6">
          Crear Estacionamientos Masivo
        </h1>

        {/* CARD */}
        <div
          className="p-8 rounded-[var(--radius)] shadow-lg"
          style={{ background: "var(--bg-card)" }}
        >
          <form onSubmit={handleSubmit} className="space-y-6">

            {/* CANTIDAD */}
            <div>
              <label className="block text-sm font-semibold mb-2">
                Cantidad de espacios
              </label>
              <input
                type="number"
                value={cantidad}
                onChange={(e) => setCantidad(e.target.value)}
                placeholder="Ejemplo: 10"
                className="
                  w-full px-4 py-3 rounded-md
                  bg-[var(--bg-alt)]
                  border border-[var(--bg-alt)]
                  focus:border-[var(--primary)]
                  focus:ring-2 focus:ring-[var(--primary)]
                  transition
                "
              />
            </div>

            {/* TIPO */}
            <div>
              <label className="block text-sm font-semibold mb-2">
                Tipo de Estacionamiento
              </label>
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

            {/* BOTÓN CREAR */}
            <button
              type="submit"
              className="
                w-full py-3 rounded-md text-center
                button
                bg-[var(--primary)]
                hover:bg-[var(--primary-dark)]
                font-semibold
              "
            >
              Crear Estacionamientos
            </button>

            {/* BOTÓN CANCELAR */}
            <Link
              href="/estacionamientos/listar"
              className="
                w-full block text-center py-3 mt-2 rounded-md
                button-danger
                font-semibold
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
