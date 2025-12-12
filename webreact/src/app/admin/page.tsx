"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";

export default function HomeAdmin() {
  const [estacionamientos, setEstacionamientos] = useState<any[]>([]);
  const [ocupados, setOcupados] = useState<any[]>([]);
  const [disponibles, setDisponibles] = useState(0);

  const [patenteIngreso, setPatenteIngreso] = useState("");
  const [patenteSalida, setPatenteSalida] = useState("");
  const [modo, setModo] = useState("cualquiera");
  const [espacioSeleccionado, setEspacioSeleccionado] = useState("");

  /* =========================
     CARGA INICIAL
  ========================= */
  const cargarDatos = async () => {
    try {
      const { data } = await api.get("/estacionamientos/");

      setEstacionamientos(data);
      setDisponibles(data.filter((e: any) => e.estado === "D").length);

      setOcupados(
        data
          .filter((e: any) => e.estado === "O")
          .map((e: any) => ({
            id: e.id,
            patente: e.patente,
            fecha_inicio: e.fechaInicio
              ? new Date(e.fechaInicio).toLocaleTimeString()
              : "--",
          }))
      );
    } catch (error) {
      console.error(error);
      alert("Error al cargar datos");
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  /* =========================
     INGRESO
  ========================= */
  const ingresarVehiculo = async (e: any) => {
    e.preventDefault();

    const patente = patenteIngreso.trim().toUpperCase();

    if (!patente) {
      alert("Debe ingresar patente");
      return;
    }

    // Validar patente duplicada
    const yaExiste = estacionamientos.some(
      (e) => e.estado === "O" && e.patente === patente
    );

    if (yaExiste) {
      alert("Esta patente ya se encuentra estacionada");
      return;
    }

    let id: number | null = null;

    if (modo === "cualquiera") {
      const libre = estacionamientos.find((e) => e.estado === "D");
      id = libre?.id;
    } else {
      id = Number(espacioSeleccionado);
    }

    if (!id) {
      alert("No hay espacios disponibles");
      return;
    }

    try {
      await api.post(`/estacionamientos/${id}/ocupar/`, {
        patente,
      });

      alert("Vehículo ingresado correctamente");

      setPatenteIngreso("");
      setEspacioSeleccionado("");
      cargarDatos();
    } catch (error) {
      console.error(error);
      alert("Error al ingresar vehículo");
    }
  };

  /* =========================
     SALIDA POR PATENTE
  ========================= */
  const salidaPorPatente = async (e: any) => {
    e.preventDefault();

    const patente = patenteSalida.trim().toUpperCase();

    if (!patente) {
      alert("Debe ingresar una patente");
      return;
    }

    const estacionamiento = estacionamientos.find(
      (e) => e.patente === patente
    );

    if (!estacionamiento) {
      alert("Patente no encontrada");
      return;
    }

    const confirmar = confirm(
      `¿Desea finalizar la salida del vehículo ${patente}?`
    );

    if (!confirmar) return;

    try {
      await api.post(`/estacionamientos/${estacionamiento.id}/liberar/`);
      alert("Salida registrada correctamente");
      setPatenteSalida("");
      cargarDatos();
    } catch (error) {
      console.error(error);
      alert("Error al liberar el espacio");
    }
  };

  /* =========================
     MARCAR SALIDA DESDE TABLA
  ========================= */
  const marcarSalida = async (id: number) => {
    const confirmar = confirm(
      "¿Está seguro que desea marcar la salida de este vehículo?"
    );

    if (!confirmar) return;

    try {
      await api.post(`/estacionamientos/${id}/liberar/`);
      alert("Salida registrada");
      cargarDatos();
    } catch (error) {
      console.error(error);
      alert("Error al marcar salida");
    }
  };

  /* =========================
     JSX — SIN CAMBIOS
  ========================= */
  return (
    <main className="p-6 min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <h1 className="text-3xl font-bold mb-10 text-center">
        Panel de Gestión de Estacionamiento
      </h1>

      {/* DISPONIBILIDAD */}
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

      {/* INGRESO / SALIDA */}
      <section
        className="p-6 mb-10 rounded-xl shadow-lg"
        style={{ background: "var(--bg-card)" }}
      >
        <h2 className="text-2xl font-semibold mb-6">Control de vehículos</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          {/* INGRESO */}
          <div>
            <h3 className="text-xl font-semibold mb-4">Ingresar vehículo</h3>

            <form className="flex flex-col gap-4" onSubmit={ingresarVehiculo}>
              <input
                type="text"
                placeholder="Patente"
                value={patenteIngreso}
                onChange={(e) =>
                  setPatenteIngreso(e.target.value.toUpperCase())
                }
                className="px-4 py-3 bg-[var(--bg-alt)] border border-[var(--bg-alt)] rounded-lg"
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
                  value={espacioSeleccionado}
                  onChange={(e) => setEspacioSeleccionado(e.target.value)}
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
                className="py-3 rounded-lg bg-[var(--primary)] font-semibold"
              >
                Ingresar vehículo
              </button>
            </form>
          </div>

          {/* SALIDA */}
          <div>
            <h3 className="text-xl font-semibold mb-4">Salida por patente</h3>

            <form className="flex flex-col gap-4" onSubmit={salidaPorPatente}>
              <input
                type="text"
                placeholder="Ej: ABC123"
                value={patenteSalida}
                onChange={(e) =>
                  setPatenteSalida(e.target.value.toUpperCase())
                }
                className="px-4 py-3 bg-[var(--bg-alt)] border border-[var(--bg-alt)] rounded-lg"
              />

              <button
                type="submit"
                className="py-3 rounded-lg bg-[var(--danger)] font-semibold"
              >
                Finalizar salida
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* OCUPADOS */}
      <section
        className="p-6 rounded-xl shadow-lg"
        style={{ background: "var(--bg-card)" }}
      >
        <h2 className="text-2xl font-semibold mb-6">Espacios ocupados</h2>

        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-[var(--bg-alt)]">
              <th className="px-4 py-3">Espacio</th>
              <th className="px-4 py-3">Patente</th>
              <th className="px-4 py-3">Hora ingreso</th>
              <th className="px-4 py-3">Acción</th>
            </tr>
          </thead>

          <tbody>
            {ocupados.length ? (
              ocupados.map((e) => (
                <tr key={e.id}>
                  <td className="px-4 py-3 font-semibold">#{e.id}</td>
                  <td className="px-4 py-3">{e.patente}</td>
                  <td className="px-4 py-3">{e.fecha_inicio}</td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => marcarSalida(e.id)}
                      className="px-4 py-2 rounded-lg bg-[var(--danger)]"
                    >
                      Marcar salida
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="text-center py-4 opacity-60">
                  No hay vehículos estacionados
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </section>
    </main>
  );
}
