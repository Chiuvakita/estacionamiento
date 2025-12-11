"use client";

import NavbarCliente from "@/components/NavbarCliente";
import Link from "next/link";

export default function CrearVehiculoPage() {
  const handleSubmit = (e: any) => {
    e.preventDefault();
    alert("Vehículo creado correctamente (simulación)");
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarCliente />

      <main className="max-w-xl mx-auto p-8">
        <h1 className="text-3xl font-bold mb-6 text-center">Crear Vehículo</h1>

        <div
          className="p-6 rounded-[var(--radius)] shadow-lg"
          style={{ background: "var(--bg-card)" }}
        >
          <form onSubmit={handleSubmit} className="space-y-4">

            {/* Patente */}
            <div>
              <label className="block mb-1 text-[var(--text-light)]">Patente</label>
              <input
                type="text"
                className="w-full p-3 rounded-md bg-[var(--bg-alt)]"
                placeholder="AAA-123"
              />
            </div>

            {/* Marca */}
            <div>
              <label className="block mb-1 text-[var(--text-light)]">Marca</label>
              <input
                type="text"
                className="w-full p-3 rounded-md bg-[var(--bg-alt)]"
                placeholder="Toyota"
              />
            </div>

            {/* Modelo */}
            <div>
              <label className="block mb-1 text-[var(--text-light)]">Modelo</label>
              <input
                type="text"
                className="w-full p-3 rounded-md bg-[var(--bg-alt)]"
                placeholder="Corolla"
              />
            </div>

            {/* Tipo */}
            <div>
              <label className="block mb-1 text-[var(--text-light)]">Tipo</label>
              <select className="w-full p-3 rounded-md bg-[var(--bg-alt)]">
                <option value="Auto">Auto</option>
                <option value="Moto">Moto</option>
                <option value="Camioneta">Camioneta</option>
              </select>
            </div>

            {/* Botones */}
            <div className="flex gap-3 mt-4">
              <button
                type="submit"
                className="flex-1 py-3 rounded-md bg-[var(--success)] hover:bg-[var(--success-dark)]"
              >
                Guardar
              </button>

              <Link
                href="/vehiculos/listar"
                className="flex-1 py-3 text-center rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)]"
              >
                Cancelar
              </Link>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}
