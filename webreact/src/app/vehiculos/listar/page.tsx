"use client";

import NavbarCliente from "@/components/NavbarCliente";
import Link from "next/link";
import { useEffect, useState } from "react";
import {
  listarVehiculos,
  eliminarVehiculo as eliminarVehiculoAPI,
  eliminarTodosVehiculos,
  Vehiculo,
} from "@/services/vehiculos";
import api from "@/services/api";

export default function ListarVehiculosPage() {
  const [vehiculos, setVehiculos] = useState<Vehiculo[]>([]);
  const [loading, setLoading] = useState(true);

  const cargarVehiculos = async () => {
    try {
      setLoading(true);
      const data = await listarVehiculos();
      setVehiculos(data);
    } catch (error) {
      console.error(error);
      alert("Error al cargar vehículos");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarVehiculos();
  }, []);

  const eliminarVehiculo = async (id: number) => {
    if (!confirm("¿Eliminar este vehículo?")) return;

    try {
      await eliminarVehiculoAPI(id);
      setVehiculos((prev) => prev.filter((v) => v.id !== id));
    } catch (error) {
      console.error(error);
      alert("No se pudo eliminar el vehículo");
    }
  };

  const eliminarTodos = async () => {
    if (!confirm("¿Eliminar TODOS tus vehículos? Esta acción no se puede deshacer.")) {
      return;
    }

    try {
      for (const v of vehiculos) {
        await api.delete(`vehiculos/${v.id}/`);
      }

      alert("Todos los vehículos fueron eliminados");
      setVehiculos([]);
    } catch (error) {
      console.error(error);
      alert("Error al eliminar vehículos");
    }
  };



  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarCliente />

      <main className="max-w-5xl mx-auto p-8">
        <h1 className="text-3xl font-bold text-center mb-6">
          Listado de Vehículos
        </h1>

        {/* Acciones */}
        <div className="flex gap-4 mb-6 flex-wrap">
          <Link
            href="/reservas/listar"
            className="px-5 py-2 rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)]"
          >
            Volver
          </Link>

          <Link
            href="/vehiculos/crear"
            className="px-5 py-2 rounded-md bg-[var(--success)] hover:bg-[var(--success-dark)]"
          >
            Crear
          </Link>

          <button
            onClick={eliminarTodos}
            className="px-5 py-2 rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)]"
          >
            Eliminar todos
          </button>

        </div>

        {/* Tabla */}
        <div
          className="rounded-[var(--radius)] overflow-hidden shadow"
          style={{ background: "var(--bg-card)" }}
        >
          <table className="w-full border-collapse">
            <thead className="bg-[var(--bg-alt)]">
              <tr>
                <th className="p-3 text-left text-[var(--text-light)]">ID</th>
                <th className="p-3 text-left">Patente</th>
                <th className="p-3 text-left">Marca</th>
                <th className="p-3 text-left">Modelo</th>
                <th className="p-3 text-left">Tipo</th>
                <th className="p-3 text-left">Acciones</th>
              </tr>
            </thead>

            <tbody>
              {!loading && vehiculos.length === 0 && (
                <tr>
                  <td
                    colSpan={6}
                    className="p-4 text-center text-[var(--text-light)]"
                  >
                    No hay vehículos registrados.
                  </td>
                </tr>
              )}

              {vehiculos.map((v) => (
                <tr key={v.id} className="hover:bg-[#2d3748] transition">
                  <td className="p-3">{v.id}</td>
                  <td className="p-3">{v.patente}</td>
                  <td className="p-3">{v.marca}</td>
                  <td className="p-3">{v.modelo}</td>
                  <td className="p-3">{v.tipo}</td>

                  <td className="p-3 flex gap-2">
                    <Link
                      href={`/vehiculos/editar/${v.id}`}
                      className="px-3 py-2 rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)]"
                    >
                      Editar
                    </Link>

                    <button
                      onClick={() => eliminarVehiculo(v.id)}
                      className="px-3 py-2 rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)]"
                    >
                      Eliminar
                    </button>
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
