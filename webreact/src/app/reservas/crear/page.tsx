"use client";

import NavbarCliente from "@/components/NavbarCliente";
import Link from "next/link";
import { useState } from "react";

export default function CrearReservaPage() {
  const [vehiculo, setVehiculo] = useState("");
  const [fechaInicio, setFechaInicio] = useState("");
  const [duracion, setDuracion] = useState("");
  const [estacionamiento, setEstacionamiento] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!vehiculo || !fechaInicio || !duracion || !estacionamiento) {
      alert("Debe completar todos los campos.");
      return;
    }

    alert("Reserva creada (simulación).");
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarCliente />

      <main className="max-w-xl mx-auto p-6 pt-10">
        <h1 className="text-3xl font-bold text-center mb-6">Crear Reserva</h1>

        <div
          className="p-8 rounded-[var(--radius)] shadow-lg"
          style={{ background: "var(--bg-card)" }}
        >
          <form onSubmit={handleSubmit} className="space-y-6">

            {/* Vehículo */}
            <div>
              <label className="block text-sm font-semibold mb-2">Vehículo</label>
              <select
                value={vehiculo}
                onChange={(e) => setVehiculo(e.target.value)}
                className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)] transition"
              >
                <option value="">Seleccione su vehículo</option>
                <option value="AAAA11">AAAA11</option>
                <option value="BBBB22">BBBB22</option>
              </select>
            </div>

            {/* Fecha inicio */}
            <div>
              <label className="block text-sm font-semibold mb-2">Fecha de inicio</label>
              <input
                type="datetime-local"
                value={fechaInicio}
                onChange={(e) => setFechaInicio(e.target.value)}
                className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)] transition"
              />
            </div>

            {/* Duración */}
            <div>
              <label className="block text-sm font-semibold mb-2">Duración (minutos)</label>
              <input
                type="number"
                value={duracion}
                onChange={(e) => setDuracion(e.target.value)}
                className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)] transition"
              />
            </div>

            {/* Estacionamiento */}
            <div>
              <label className="block text-sm font-semibold mb-2">Estacionamiento</label>
              <select
                value={estacionamiento}
                onChange={(e) => setEstacionamiento(e.target.value)}
                className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)] focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)] transition"
              >
                <option value="">Seleccione</option>
                <option value="1">Espacio #1</option>
                <option value="2">Espacio #2</option>
              </select>
            </div>

            {/* Botones */}
            <button className="w-full py-3 rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)] font-semibold transition">
              Guardar
            </button>

            <Link
              href="/reservas/listar"
              className="w-full block text-center py-3 rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)] font-semibold transition"
            >
              Cancelar
            </Link>
          </form>
        </div>
      </main>
    </div>
  );
}
