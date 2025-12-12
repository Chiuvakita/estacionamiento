"use client";

import NavbarCliente from "@/components/NavbarCliente";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { listarVehiculos } from "@/services/vehiculos";
import { listarEstacionamientosDisponibles } from "@/services/reservas";

export default function CrearReservaPage() {
  const router = useRouter();

  const [vehiculos, setVehiculos] = useState<any[]>([]);
  const [estacionamientos, setEstacionamientos] = useState<any[]>([]);
  const [loadingEspacios, setLoadingEspacios] = useState(true);

  const [vehiculoId, setVehiculoId] = useState("");
  const [fechaInicio, setFechaInicio] = useState("");
  const [duracion, setDuracion] = useState("");
  const [estacionamiento, setEstacionamiento] = useState("");

  /* =========================
     CARGAR VEHÍCULOS CLIENTE
  ========================= */
  useEffect(() => {
    const cargarVehiculos = async () => {
      try {
        const data = await listarVehiculos();
        setVehiculos(data);

        // Guardamos para reutilizar en reservas
        localStorage.setItem("vehiculos_cliente", JSON.stringify(data));
      } catch (error) {
        console.error(error);
        alert("Error al cargar vehículos");
      }
    };

    cargarVehiculos();
  }, []);

  /* =========================
     CARGAR ESTACIONAMIENTOS
  ========================= */
  useEffect(() => {
    const cargarEspacios = async () => {
      try {
        const data = await listarEstacionamientosDisponibles();
        setEstacionamientos(data);
      } catch (error) {
        console.error(error);
        alert("Error al cargar estacionamientos");
      } finally {
        setLoadingEspacios(false);
      }
    };

    cargarEspacios();
  }, []);

  /* =========================
     CREAR RESERVA
  ========================= */
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!vehiculoId || !fechaInicio || !duracion || !estacionamiento) {
      alert("Debe completar todos los campos.");
      return;
    }

    const duracionMin = Number(duracion);

    // ⏱ Máx 3 horas
    if (duracionMin > 180) {
      alert("La duración máxima permitida es de 3 horas (180 minutos).");
      return;
    }

    const reservasActuales = JSON.parse(
      localStorage.getItem("reservas_cliente") || "[]"
    );

    // ❌ No permitir más de una reserva activa
    const reservaActiva = reservasActuales.find(
      (r: any) => r.restante !== "Finalizada"
    );

    if (reservaActiva) {
      alert(
        "Ya tienes una reserva activa.\nDebes finalizarla antes de crear otra."
      );
      return;
    }

    const vehiculo = vehiculos.find(
      (v) => v.id === Number(vehiculoId)
    );

    if (!vehiculo) {
      alert("Vehículo inválido");
      return;
    }

    if (estacionamientos.length === 0) {
      alert("No hay estacionamientos disponibles.");
      return;
    }

    const nuevaReserva = {
      id: Date.now(),
      vehiculoId: vehiculo.id,
      patente: vehiculo.patente,
      estacionamiento: Number(estacionamiento),
      fechaInicio,
      fechaTermino: null,
      duracion: duracionMin,
      restante: `${duracionMin} min`,
    };

    reservasActuales.push(nuevaReserva);

    localStorage.setItem(
      "reservas_cliente",
      JSON.stringify(reservasActuales)
    );

    alert("Reserva creada correctamente");
    router.push("/reservas/listar");
  };

  /* =========================
     JSX
  ========================= */
  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarCliente />

      <main className="max-w-xl mx-auto p-6 pt-10">
        <h1 className="text-3xl font-bold text-center mb-6">
          Crear Reserva
        </h1>

        <div
          className="p-8 rounded-[var(--radius)] shadow-lg"
          style={{ background: "var(--bg-card)" }}
        >
          <form onSubmit={handleSubmit} className="space-y-6">

            {/* VEHÍCULO */}
            <div>
              <label className="block text-sm font-semibold mb-2">
                Vehículo
              </label>

              <select
                value={vehiculoId}
                onChange={(e) => setVehiculoId(e.target.value)}
                className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)]"
              >
                <option value="">Seleccione su vehículo</option>
                {vehiculos.map((v) => (
                  <option key={v.id} value={v.id}>
                    {v.patente} — {v.marca} {v.modelo}
                  </option>
                ))}
              </select>

              {vehiculos.length === 0 && (
                <p className="text-sm mt-2 text-[var(--danger)]">
                  Debe registrar un vehículo antes de crear una reserva.
                </p>
              )}
            </div>

            {/* FECHA INICIO */}
            <div>
              <label className="block text-sm font-semibold mb-2">
                Fecha de inicio
              </label>
              <input
                type="datetime-local"
                value={fechaInicio}
                onChange={(e) => setFechaInicio(e.target.value)}
                className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)]"
              />
            </div>

            {/* DURACIÓN */}
            <div>
              <label className="block text-sm font-semibold mb-2">
                Duración (minutos)
              </label>
              <input
                type="number"
                min={1}
                value={duracion}
                onChange={(e) => setDuracion(e.target.value)}
                className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)]"
              />
            </div>

            {/* ESTACIONAMIENTO */}
            <div>
              <label className="block text-sm font-semibold mb-2">
                Estacionamiento
              </label>

              <select
                value={estacionamiento}
                onChange={(e) => setEstacionamiento(e.target.value)}
                disabled={loadingEspacios || estacionamientos.length === 0}
                className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)]"
              >
                <option value="">Seleccione</option>
                {estacionamientos.map((e) => (
                  <option key={e.id} value={e.id}>
                    Espacio #{e.id} — {e.tipo}
                  </option>
                ))}
              </select>

              {!loadingEspacios && estacionamientos.length === 0 && (
                <p className="text-sm mt-2 text-[var(--danger)]">
                  No hay estacionamientos disponibles en este momento.
                </p>
              )}
            </div>

            {/* BOTONES */}
            <button
              type="submit"
              disabled={vehiculos.length === 0}
              className="w-full py-3 rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)] font-semibold disabled:opacity-50"
            >
              Guardar
            </button>

            <Link
              href="/reservas/listar"
              className="w-full block text-center py-3 rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)] font-semibold"
            >
              Cancelar
            </Link>

          </form>
        </div>
      </main>
    </div>
  );
}
