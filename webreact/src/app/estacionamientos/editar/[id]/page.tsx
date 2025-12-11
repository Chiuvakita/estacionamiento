"use client";

import NavbarAdmin from "@/components/NavbarAdmin";
import Link from "next/link";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";

export default function EditarEstacionamientoPage() {
  const { id } = useParams(); // ← ID del estacionamiento desde la URL

  const [loading, setLoading] = useState(true);

  const [estado, setEstado] = useState("");
  const [tipo, setTipo] = useState("");
  const [patente, setPatente] = useState("");

  // Simulación de obtener datos del backend
  useEffect(() => {
    setTimeout(() => {
      // Datos simulados según el ID
      setEstado("L");
      setTipo("Auto");
      setPatente("ABCD12");

      setLoading(false);
    }, 300);
  }, [id]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (patente.trim() === "") {
      alert("Debe ingresar una patente válida o '-'.");
      return;
    }

    alert(`Editando estacionamiento #${id}
Estado: ${estado}
Tipo: ${tipo}
Patente: ${patente}`);
  };

  if (loading) {
    return (
      <div className="text-center text-[var(--text)] mt-20">
        Cargando datos...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-xl mx-auto p-6 mt-6">
        <h1 className="text-3xl font-bold text-center mb-6">
          Editar Estacionamiento #{id}
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

            {/* BOTÓN GUARDAR */}
            <button
              type="submit"
              className="
                w-full py-3 rounded-md text-center
                font-semibold
                bg-[var(--primary)]
                hover:bg-[var(--primary-dark)]
                transition
              "
            >
              Guardar Cambios
            </button>

            {/* BOTÓN CANCELAR */}
            <Link
              href="/estacionamientos/listar"
              className="
                w-full block text-center py-3 mt-2 rounded-md
                font-semibold
                bg-[var(--danger)]
                hover:bg-[var(--danger-dark)]
                transition
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
