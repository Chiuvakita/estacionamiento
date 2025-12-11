"use client";

import NavbarAdmin from "@/components/NavbarAdmin";
import { useEffect, useState } from "react";

// Simulación de API
const mockHistorial = [
  {
    estacionamiento_id: 1,
    movimientos: [
      {
        id: 1,
        patente: "ABCD12",
        fecha_inicio: "2025-01-01 10:00",
        fecha_termino: "2025-01-01 12:00",
        es_reserva: true,
      },
      {
        id: 2,
        patente: "EFGH34",
        fecha_inicio: "2025-01-02 09:00",
        fecha_termino: null,
        es_reserva: false,
      },
    ],
  },
  {
    estacionamiento_id: 2,
    movimientos: [
      {
        id: 1,
        patente: "ZZZZ99",
        fecha_inicio: "2025-01-03 15:00",
        fecha_termino: "2025-01-03 17:00",
        es_reserva: true,
      },
    ],
  },
];

export default function HistorialListarPage() {
  const [historial, setHistorial] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setHistorial(mockHistorial);
      setLoading(false);
    }, 300);
  }, []);

  if (loading) {
    return (
      <div className="text-center text-[var(--text)] mt-20">
        Cargando historial...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-5xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-center mb-6">
          Historial de Movimientos
        </h1>

        <p className="mb-8 text-lg text-center">
          <strong>Total de reservas registradas:</strong>{" "}
          {historial.reduce(
            (total, grupo) =>
              total +
              grupo.movimientos.filter((m: any) => m.es_reserva).length,
            0
          )}
        </p>

        {/* Lista por espacio */}
        {historial.length === 0 ? (
          <p className="text-center text-gray-400">No hay registros disponibles.</p>
        ) : (
          historial.map((grupo) => (
            <div
              key={grupo.estacionamiento_id}
              className="mb-8 rounded-[var(--radius)] shadow p-6"
              style={{ background: "var(--bg-card)" }}
            >
              <h2 className="text-2xl mb-4">
                Espacio #{grupo.estacionamiento_id}
              </h2>

              <div className="overflow-x-auto rounded-[var(--radius)]">
                <table className="w-full border-collapse">
                  <thead className="bg-[var(--bg-alt)] text-[var(--text-light)]">
                    <tr>
                      <th className="p-3 text-left">#</th>
                      <th className="p-3 text-left">Patente</th>
                      <th className="p-3 text-left">Inicio</th>
                      <th className="p-3 text-left">Término</th>
                      <th className="p-3 text-left">Reserva</th>
                    </tr>
                  </thead>

                  <tbody>
                    {grupo.movimientos.map((m: any, index: number) => (
                      <tr
                        key={index}
                        className="border-b border-[var(--bg-alt)] hover:bg-[#2d3748]"
                      >
                        <td className="p-3">{index + 1}</td>
                        <td className="p-3">{m.patente}</td>
                        <td className="p-3">{m.fecha_inicio}</td>
                        <td className="p-3">
                          {m.fecha_termino ? (
                            m.fecha_termino
                          ) : (
                            <span className="text-yellow-400">En uso</span>
                          )}
                        </td>
                        <td className="p-3">
                          {m.es_reserva ? (
                            <span className="text-green-400 font-semibold">SI</span>
                          ) : (
                            <span className="text-red-400 font-semibold">NO</span>
                          )}
                        </td>
                      </tr>
                    ))}

                    {grupo.movimientos.length === 0 && (
                      <tr>
                        <td
                          colSpan={5}
                          className="text-center text-gray-500 p-4"
                        >
                          Sin movimientos
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          ))
        )}
      </main>
    </div>
  );
}
