"use client";

import { useState } from "react";

export default function HomeAdmin() {
  const [disponibles] = useState(12);

  const [estacionamientos] = useState([
    { id: 1, estado: "D", tipo: "Auto" },
    { id: 2, estado: "O", tipo: "Moto" },
    { id: 3, estado: "D", tipo: "Auto" },
  ]);

  const [ocupados] = useState([
    { id: 2, patente: "ABC123", fecha_inicio: "10:30" },
    { id: 5, patente: "XYZ987", fecha_inicio: "11:10" },
  ]);

  const [modo, setModo] = useState("cualquiera");

  return (
    <main className="p-6 min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <h1 className="text-3xl font-bold mb-10 text-center">
        Panel de Gestión de Estacionamiento
      </h1>

      {/* =======================
          DISPONIBILIDAD
        ======================= */}
      <section
        className="p-6 mb-10 rounded-xl shadow-lg"
        style={{ background: "var(--bg-card)" }}
      >
        <h2 className="text-2xl font-semibold mb-3">Disponibilidad actual</h2>

        <div className="mt-3 text-lg">
          <span className="font-semibold text-[var(--success)]">
            {disponibles}
          </span>{" "}
          espacios disponibles
        </div>
      </section>

      {/* =======================
          INGRESO / SALIDA
        ======================= */}
      <section
        className="p-6 mb-10 rounded-xl shadow-lg"
        style={{ background: "var(--bg-card)" }}
      >
        <h2 className="text-2xl font-semibold mb-6">Control de vehículos</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">

          {/* INGRESO */}
          <div>
            <h3 className="text-xl font-semibold mb-4">Ingresar vehículo</h3>

            <form className="flex flex-col gap-4">
              <input
                type="text"
                placeholder="Patente"
                className="px-4 py-3 bg-[var(--bg-alt)] border border-[var(--bg-alt)] rounded-lg 
                           focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)] outline-none"
              />

              <label className="font-semibold">Modo de asignación</label>

              <select
                className="px-4 py-3 bg-[var(--bg-alt)] border border-[var(--bg-alt)] rounded-lg"
                value={modo}
                onChange={(e) => setModo(e.target.value)}
              >
                <option value="cualquiera">Asignación automática</option>
                <option value="especifico">Seleccionar espacio</option>
              </select>

              {modo === "especifico" && (
                <select
                  className="px-4 py-3 bg-[var(--bg-alt)] border border-[var(--bg-alt)] rounded-lg"
                >
                  {estacionamientos
                    .filter((e) => e.estado === "D")
                    .map((e) => (
                      <option key={e.id} value={e.id}>
                        Espacio #{e.id} — {e.tipo}
                      </option>
                    ))}
                </select>
              )}

              <button
                type="submit"
                className="py-3 rounded-lg bg-[var(--primary)] hover:bg-[var(--primary-dark)] 
                           transition-transform font-semibold hover:scale-[1.03]"
              >
                Ingresar vehículo
              </button>
            </form>
          </div>

          {/* SALIDA */}
          <div>
            <h3 className="text-xl font-semibold mb-4">Salida por patente</h3>

            <form className="flex flex-col gap-4">
              <input
                type="text"
                placeholder="Ej: ABC123"
                className="px-4 py-3 bg-[var(--bg-alt)] border border-[var(--bg-alt)] rounded-lg 
                           focus:border-[var(--primary)] focus:ring-2 focus:ring-[var(--primary)] outline-none"
              />

              <button
                type="submit"
                className="py-3 rounded-lg bg-[var(--danger)] hover:bg-[var(--danger-dark)] 
                           transition-transform font-semibold hover:scale-[1.03]"
              >
                Finalizar salida
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* =======================
          OCUPADOS
        ======================= */}
      <section
        className="p-6 rounded-xl shadow-lg"
        style={{ background: "var(--bg-card)" }}
      >
        <h2 className="text-2xl font-semibold mb-6">Espacios ocupados</h2>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-[var(--bg-alt)] text-[var(--text-light)]">
                <th className="px-4 py-3">Espacio</th>
                <th className="px-4 py-3">Patente</th>
                <th className="px-4 py-3">Hora ingreso</th>
                <th className="px-4 py-3">Acción</th>
              </tr>
            </thead>

            <tbody>
              {ocupados.length ? (
                ocupados.map((e) => (
                  <tr key={e.id} className="border-b border-[var(--bg-alt)]">
                    <td className="px-4 py-3 font-semibold">#{e.id}</td>
                    <td className="px-4 py-3">{e.patente}</td>
                    <td className="px-4 py-3">{e.fecha_inicio}</td>
                    <td className="px-4 py-3">
                      <button
                        className="px-4 py-2 rounded-lg bg-[var(--danger)] hover:bg-[var(--danger-dark)] 
                                   transition-transform hover:scale-[1.03]"
                      >
                        Marcar salida
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan={4}
                    className="py-4 text-center text-[var(--text-light)]"
                  >
                    No hay vehículos estacionados
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
