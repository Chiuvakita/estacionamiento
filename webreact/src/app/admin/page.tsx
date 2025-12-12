"use client";

import { useEffect, useState } from "react";
import NavbarAdmin from "@/components/NavbarAdmin";
import api from "@/services/api";

interface Estacionamiento {
  id: number;
  estado: "D" | "O";
  tipo: string;
  patente: string | null;
  fechaInicio?: string;
}

export default function HomeAdmin() {
  const [estacionamientos, setEstacionamientos] = useState<Estacionamiento[]>([]);
  const [patenteIngreso, setPatenteIngreso] = useState("");
  const [modo, setModo] = useState<"cualquiera" | "especifico">("cualquiera");
  const [espacioSeleccionado, setEspacioSeleccionado] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  /* =========================
     CARGA INICIAL
  ========================= */
  const cargarEstacionamientos = async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/estacionamientos/");
      setEstacionamientos(data);
    } catch (e) {
      console.error(e);
      alert("Error cargando estacionamientos");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarEstacionamientos();
  }, []);

  /* =========================
     DERIVADOS
  ========================= */
  const disponibles = estacionamientos.filter(e => e.estado === "D");
  const ocupados = estacionamientos.filter(e => e.estado === "O");

  /* =========================
     INGRESAR VEHÍCULO
  ========================= */
  const ingresarVehiculo = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!patenteIngreso.trim()) {
      alert("Debe ingresar patente");
      return;
    }

    let estacionamientoId: number | null = null;

    if (modo === "cualquiera") {
      estacionamientoId = disponibles[0]?.id ?? null;
    } else {
      estacionamientoId = espacioSeleccionado;
    }

    if (!estacionamientoId) {
      alert("No hay estacionamientos disponibles");
      return;
    }

    try {
      await api.post(`/estacionamientos/${estacionamientoId}/ocupar/`, {
        patente: patenteIngreso.toUpperCase(),
      });

      setPatenteIngreso("");
      setEspacioSeleccionado(null);
      cargarEstacionamientos();
    } catch (error: any) {
      console.error(error.response?.data || error);
      alert("Error al ingresar vehículo");
    }
  };

  /* =========================
     SALIDA VEHÍCULO
  ========================= */
  const liberarVehiculo = async (id: number) => {
    if (!confirm("¿Marcar salida del vehículo?")) return;

    try {
      await api.post(`/estacionamientos/${id}/liberar/`);
      cargarEstacionamientos();
    } catch (error) {
      console.error(error);
      alert("Error al liberar estacionamiento");
    }
  };

  if (loading) {
    return <div className="text-center mt-20">Cargando...</div>;
  }

  return (
    <main className="p-6 min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <h1 className="text-3xl font-bold mb-10 text-center">
        Panel de Gestión de Estacionamiento
      </h1>

      {/* =======================
          DISPONIBILIDAD
      ======================= */}
      <section className="p-6 mb-10 rounded-xl shadow-lg" style={{ background: "var(--bg-card)" }}>
        <h2 className="text-2xl font-semibold mb-3">Disponibilidad actual</h2>
        <div className="text-lg">
          <span className="font-semibold text-[var(--success)]">
            {disponibles.length}
          </span>{" "}
          espacios disponibles
        </div>
      </section>

      {/* =======================
          INGRESO
      ======================= */}
      <section className="p-6 mb-10 rounded-xl shadow-lg" style={{ background: "var(--bg-card)" }}>
        <h2 className="text-2xl font-semibold mb-6">Ingreso de vehículo</h2>

        <form onSubmit={ingresarVehiculo} className="flex flex-col gap-4 max-w-md">
          <input
            type="text"
            placeholder="Patente"
            value={patenteIngreso}
            onChange={(e) => setPatenteIngreso(e.target.value.toUpperCase())}
            className="px-4 py-3 bg-[var(--bg-alt)] border rounded-lg"
          />

          <label className="font-semibold">Modo de asignación</label>
          <select
            value={modo}
            onChange={(e) => setModo(e.target.value as any)}
            className="px-4 py-3 bg-[var(--bg-alt)] border rounded-lg"
          >
            <option value="cualquiera">Automática</option>
            <option value="especifico">Seleccionar espacio</option>
          </select>

          {modo === "especifico" && (
            <select
              value={espacioSeleccionado ?? ""}
              onChange={(e) => setEspacioSeleccionado(Number(e.target.value))}
              className="px-4 py-3 bg-[var(--bg-alt)] border rounded-lg"
            >
              <option value="">Seleccione espacio</option>
              {disponibles.map(e => (
                <option key={e.id} value={e.id}>
                  #{e.id} — {e.tipo}
                </option>
              ))}
            </select>
          )}

          <button className="py-3 rounded-lg bg-[var(--primary)] font-semibold">
            Ingresar vehículo
          </button>
        </form>
      </section>

      {/* =======================
          OCUPADOS
      ======================= */}
      <section className="p-6 rounded-xl shadow-lg" style={{ background: "var(--bg-card)" }}>
        <h2 className="text-2xl font-semibold mb-6">Espacios ocupados</h2>

        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-[var(--bg-alt)]">
              <th className="p-3">Espacio</th>
              <th className="p-3">Patente</th>
              <th className="p-3">Acción</th>
            </tr>
          </thead>

          <tbody>
            {ocupados.length ? (
              ocupados.map(e => (
                <tr key={e.id} className="border-b">
                  <td className="p-3 font-semibold">#{e.id}</td>
                  <td className="p-3">{e.patente}</td>
                  <td className="p-3">
                    <button
                      onClick={() => liberarVehiculo(e.id)}
                      className="px-4 py-2 rounded-lg bg-[var(--danger)]"
                    >
                      Marcar salida
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={3} className="text-center py-4 opacity-60">
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
