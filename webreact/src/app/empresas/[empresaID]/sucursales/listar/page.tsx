"use client";

import React, { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import NavbarAdmin from "@/components/NavbarAdmin";

export default function SucursalesListarPage() {
  const { empresaID } = useParams();
  const [sucursales, setSucursales] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Simula carga de API
  useEffect(() => {
    setTimeout(() => {
      setSucursales([
        {
          id: 1,
          nombreSucursal: "Sucursal Centro",
          direccion: "Av. Principal 123",
          numero: "+56911112222",
          cantidadEstacionamiento: 12,
        },
        {
          id: 2,
          nombreSucursal: "Sucursal Norte",
          direccion: "Ruta 5 Norte Km 5",
          numero: "+56933334444",
          cantidadEstacionamiento: 8,
        },
      ]);
      setLoading(false);
    }, 300);
  }, [empresaID]);

  const toggleOpen = (id: number) => {
    setSucursales((prev) =>
      prev.map((suc) =>
        suc.id === id ? { ...suc, open: !suc.open } : suc
      )
    );
  };

  if (loading) {
    return <div className="text-center text-[var(--text)] mt-20">Cargando...</div>;
  }

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-4xl mx-auto p-6">
        {/* Actions */}
        <div className="flex gap-4 mb-6">
          <Link
            href="/empresas/listar"
            className="px-5 py-2 rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)]"
          >
            Volver
          </Link>

          <Link
            href={`/empresas/${empresaID}/sucursales/crear`}
            className="px-5 py-2 rounded-md bg-[var(--success)] hover:bg-[var(--success-dark)]"
          >
            Crear nueva sucursal
          </Link>
        </div>

        <h1 className="text-3xl font-bold mb-4 text-center">Listado de Sucursales</h1>

        {/* Tabla */}
        <div
          className="rounded-[var(--radius)] shadow overflow-hidden"
          style={{ background: "var(--bg-card)" }}
        >
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-[var(--bg-alt)]">
                <th className="p-4 text-left text-[var(--text-light)]">Nombre</th>
              </tr>
            </thead>

            <tbody>
              {sucursales.map((sucursal) => (
                <React.Fragment key={sucursal.id}>
                  {/* Fila principal */}
                  <tr
                    className="cursor-pointer hover:bg-[#2d3748] transition"
                    onClick={() => toggleOpen(sucursal.id)}
                  >
                    <td className="p-4 flex justify-between items-center">
                      <div className="flex items-center gap-2">
                        <span>{sucursal.open ? "▼" : "▶"}</span>
                        <strong>{sucursal.nombreSucursal}</strong>
                      </div>
                    </td>
                  </tr>

                  {/* Si está abierto → fila extra */}
                  {sucursal.open && (
                    <tr className="bg-[#1F2937]">
                      <td className="p-4">
                        <p><strong>Dirección:</strong> {sucursal.direccion}</p>
                        <p><strong>Número:</strong> {sucursal.numero}</p>
                        <p><strong>Cantidad Estacionamientos:</strong> {sucursal.cantidadEstacionamiento}</p>

                        <div className="flex gap-3 mt-3">
                          <Link
                            href={`/empresas/${empresaID}/sucursales/editar/${sucursal.id}`}
                            className="px-4 py-2 rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)]"
                          >
                            Editar
                          </Link>

                          <button
                            onClick={() => alert("Eliminar sucursal (simulación)")}
                            className="px-4 py-2 rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)]"
                          >
                            Eliminar
                          </button>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>

          </table>
        </div>
      </main>
    </div>
  );
}
