"use client";

import NavbarAdmin from "@/components/NavbarAdmin";
import Link from "next/link";
import { useState } from "react";
import { crearEstacionamiento } from "@/services/estacionamientos";
import { useRouter } from "next/navigation";

export default function CrearEstacionamientoPage() {
  const router = useRouter();

  const [estado, setEstado] = useState<"D" | "O">("D");
  const [tipo, setTipo] = useState<"Normal" | "VIP" | "Discapacitado">("Normal");
  const [patente, setPatente] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (estado === "O" && patente.trim() === "") {
      alert("Debe ingresar patente si el estacionamiento está ocupado");
      return;
    }

    const payload = {
      estado,
      tipo,
      patente: estado === "D" ? "" : patente.trim().toUpperCase(),
    };

    try {
      await crearEstacionamiento(payload);
      alert("Estacionamiento creado correctamente");
      router.push("/estacionamientos/listar");
    } catch (error: any) {
      console.error(error?.response?.data || error);
      alert("Error al crear estacionamiento");
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-xl mx-auto p-6 mt-6">
        <h1 className="text-3xl font-bold text-center mb-6">
          Crear Estacionamiento
        </h1>

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
                onChange={(e) => setEstado(e.target.value as "D" | "O")}
                className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)]
                  border border-[var(--bg-alt)]
                  focus:border-[var(--primary)]
                  focus:ring-2 focus:ring-[var(--primary)] transition"
              >
                <option value="D">Disponible</option>
                <option value="O">Ocupado</option>
              </select>
            </div>

            {/* TIPO */}
            <div>
              <label className="block text-sm font-semibold mb-2">Tipo</label>
              <select
                value={tipo}
                onChange={(e) =>
                  setTipo(e.target.value as "Normal" | "VIP" | "Discapacitado")
                }
                className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)]
                  border border-[var(--bg-alt)]
                  focus:border-[var(--primary)]
                  focus:ring-2 focus:ring-[var(--primary)] transition"
              >
                <option value="Normal">Normal</option>
                <option value="VIP">VIP</option>
                <option value="Discapacitado">Discapacitado</option>
              </select>
            </div>

            {/* PATENTE */}
            {estado === "O" && (
              <div>
                <label className="block text-sm font-semibold mb-2">Patente</label>
                <input
                  type="text"
                  value={patente}
                  onChange={(e) => setPatente(e.target.value.toUpperCase())}
                  placeholder="Ej: ABCD12"
                  maxLength={10}
                  className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)]
                    border border-[var(--bg-alt)]
                    focus:border-[var(--primary)]
                    focus:ring-2 focus:ring-[var(--primary)] transition uppercase"
                />
              </div>
            )}

            {/* BOTONES */}
            <button
              type="submit"
              className="w-full py-3 rounded-md bg-[var(--primary)]
                hover:bg-[var(--primary-dark)] font-semibold"
            >
              Crear Estacionamiento
            </button>

            <Link
              href="/estacionamientos/listar"
              className="w-full block text-center py-3 mt-2 rounded-md
                bg-[var(--danger)] hover:bg-[var(--danger-dark)] font-semibold"
            >
              Cancelar
            </Link>

          </form>
        </div>
      </main>
    </div>
  );
}
