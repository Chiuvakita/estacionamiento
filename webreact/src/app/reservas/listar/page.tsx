"use client";

import NavbarCliente from "@/components/NavbarCliente";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function ListarReservasPage() {
  const [reservas, setReservas] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  /* =========================
     CARGAR DESDE LOCALSTORAGE
  ========================= */
  const cargarReservas = () => {
    const data = JSON.parse(
      localStorage.getItem("reservas_cliente") || "[]"
    );

    setReservas(
      data.map((r: any) => ({
        ...r,
        fechaInicio: new Date(r.fechaInicio).toLocaleString(),
        fechaTermino: r.fechaTermino
          ? new Date(r.fechaTermino).toLocaleString()
          : "-",
      }))
    );

    setLoading(false);
  };

  useEffect(() => {
    cargarReservas();
  }, []);

  /* =========================
     TERMINAR RESERVA
  ========================= */
  const finalizar = (id: number) => {
    if (!confirm("¿Terminar esta reserva?")) return;

    const data = JSON.parse(
      localStorage.getItem("reservas_cliente") || "[]"
    );

    const actualizadas = data.map((r: any) =>
      r.id === id
        ? {
            ...r,
            fechaTermino: new Date().toISOString(),
            restante: "Finalizada",
          }
        : r
    );

    localStorage.setItem(
      "reservas_cliente",
      JSON.stringify(actualizadas)
    );

    cargarReservas();
  };

  /* =========================
     LOADING
  ========================= */
  if (loading) {
    return (
      <div className="text-center mt-20 text-[var(--text)]">
        Cargando reservas...
      </div>
    );
  }

  /* =========================
     JSX
  ========================= */
  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarCliente />

      <main className="max-w-6xl mx-auto p-8 pt-10">
        <h1 className="text-3xl font-bold text-center mb-6">
          Listado de Reservas
        </h1>

        {/* ACCIONES */}
        <div className="flex gap-4 mb-6 flex-wrap">
          <Link
            href="/reservas/crear"
            className="px-5 py-2 rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)]"
          >
            Crear Reserva
          </Link>

          <Link
            href="/vehiculos/listar"
            className="px-5 py-2 rounded-md bg-[var(--success)] hover:bg-[var(--success-dark)]"
          >
            Gestionar Autos
          </Link>
        </div>

        {/* TABLA */}
        <div
          className="rounded-[var(--radius)] shadow overflow-hidden"
          style={{ background: "var(--bg-card)" }}
        >
          <table className="w-full border-collapse">
            <thead className="bg-[var(--bg-alt)]">
              <tr>
                <th className="p-3 text-left text-[var(--text-light)]">ID</th>
                <th className="p-3 text-left">Patente</th>
                <th className="p-3 text-left">Estacionamiento</th>
                <th className="p-3 text-left">Inicio</th>
                <th className="p-3 text-left">Término</th>
                <th className="p-3 text-left">Duración</th>
                <th className="p-3 text-left">Restante</th>
                <th className="p-3 text-left">Acción</th>
              </tr>
            </thead>

            <tbody>
              {reservas.length === 0 && (
                <tr>
                  <td
                    colSpan={8}
                    className="p-4 text-center text-[var(--text-light)]"
                  >
                    No hay reservas registradas.
                  </td>
                </tr>
              )}

              {reservas.map((r) => (
                <tr key={r.id} className="hover:bg-[#2d3748] transition">
                  <td className="p-3">{r.id}</td>
                  <td className="p-3">{r.patente}</td>
                  <td className="p-3">#{r.estacionamiento}</td>
                  <td className="p-3">{r.fechaInicio}</td>
                  <td className="p-3">{r.fechaTermino}</td>
                  <td className="p-3">{r.duracion} min</td>
                  <td className="p-3">{r.restante}</td>

                  <td className="p-3">
                    {r.restante !== "Finalizada" ? (
                      <button
                        onClick={() => finalizar(r.id)}
                        className="px-4 py-2 rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)]"
                      >
                        Terminar
                      </button>
                    ) : (
                      <span className="text-[var(--text-light)]">---</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
