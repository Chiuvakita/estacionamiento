"use client";

import NavbarAdmin from "@/components/NavbarAdmin";
import { useState } from "react";
import Link from "next/link";
import { crearEstacionamientoMasivo } from "@/services/estacionamientos";
import { useRouter } from "next/navigation";

export default function CrearMasivoPage() {
  const router = useRouter();

  const [cantidad, setCantidad] = useState("");
  const [tipo, setTipo] = useState<"Normal" | "VIP" | "Discapacitado">("Normal");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const cantidadNum = Number(cantidad);

    if (!cantidad || isNaN(cantidadNum) || cantidadNum <= 0) {
      alert("La cantidad debe ser un número mayor a 0");
      return;
    }

    setLoading(true);

    try {
      await crearEstacionamientoMasivo({
        cantidad: cantidadNum,
        tipo,
      });

      alert("Estacionamientos creados correctamente");
      router.push("/estacionamientos/listar");
    } catch (error: any) {
      console.error(error?.response?.data || error);
      alert("Error al crear estacionamientos");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-xl mx-auto p-6 mt-6">
        <h1 className="text-3xl font-bold text-center mb-6">
          Crear Estacionamientos Masivo
        </h1>

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
                min={1}
                value={cantidad}
                onChange={(e) => setCantidad(e.target.value)}
                placeholder="Ej: 10"
                className="w-full px-4 py-3 rounded-md
                  bg-[var(--bg-alt)]
                  border border-[var(--bg-alt)]
                  focus:border-[var(--primary)]
                  focus:ring-2 focus:ring-[var(--primary)] transition"
              />
            </div>

            {/* TIPO */}
            <div>
              <label className="block text-sm font-semibold mb-2">
                Tipo de Estacionamiento
              </label>
              <select
                value={tipo}
                onChange={(e) =>
                  setTipo(e.target.value as "Normal" | "VIP" | "Discapacitado")
                }
                className="w-full px-4 py-3 rounded-md
                  bg-[var(--bg-alt)]
                  border border-[var(--bg-alt)]
                  focus:border-[var(--primary)]
                  focus:ring-2 focus:ring-[var(--primary)] transition"
              >
                <option value="Normal">Normal</option>
                <option value="VIP">VIP</option>
                <option value="Discapacitado">Discapacitado</option>
              </select>
            </div>

            {/* BOTÓN CREAR */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-md bg-[var(--primary)]
                hover:bg-[var(--primary-dark)] font-semibold disabled:opacity-50"
            >
              {loading ? "Creando..." : "Crear Estacionamientos"}
            </button>

            {/* CANCELAR */}
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
