"use client";

import NavbarAdmin from "@/components/NavbarAdmin";
import Link from "next/link";
import { useState, useEffect } from "react";
import {
  listarEstacionamientos,
  eliminarEstacionamiento,
  eliminarTodosEstacionamientos,
} from "@/services/estacionamientos";


export default function EstacionamientosListar() {
  const [estacionamientos, setEstacionamientos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);

    listarEstacionamientos()
      .then(setEstacionamientos)
      .catch((err) => {
        console.error("Error cargando estacionamientos", err);
      })
      .finally(() => setLoading(false));
  }, []);


  const eliminarEstacionamientoHandler = async (id: number) => {
    if (!confirm(`¿Eliminar estacionamiento #${id}?`)) return;

    try {
      await eliminarEstacionamiento(id);

      setEstacionamientos((prev) =>
        prev.filter((e) => e.id !== id)
      );

      alert("Estacionamiento eliminado");
    } catch (error) {
      console.error(error);
      alert("Error al eliminar");
    }
  };



  const eliminarTodos = async () => {
    if (!confirm("¿Eliminar TODOS los estacionamientos?")) return;

    try {
      const res = await eliminarTodosEstacionamientos();
      alert(`Eliminados ${res.eliminados} estacionamientos`);
      // recargar listado
      setEstacionamientos([]);
    } catch (error) {
      alert("Error al eliminar estacionamientos");
    }
  };




  if (loading)
    return <div className="text-center text-[var(--text)] mt-20">Cargando...</div>;

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-6xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-center mb-6">Listado de Estacionamientos</h1>

        {/* Card acciones */}
        <div
          className="p-6 rounded-[var(--radius)] shadow mb-6 flex flex-wrap gap-4"
          style={{ background: "var(--bg-card)" }}
        >
          <Link href="/estacionamientos/crear" className="button">
            Crear
          </Link>

          <Link href="/estacionamientos/crear-masivo" className="button">
            Crear masivo
          </Link>

          <button
            onClick={eliminarTodos}
            className="button button-danger"
          >
            Eliminar todos
          </button>

        </div>

        {/* Tabla */}
        <div className="rounded-[var(--radius)] shadow overflow-hidden" style={{ background: "var(--bg-card)" }}>
          <table className="w-full border-collapse">
            <thead className="bg-[var(--bg-alt)] text-[var(--text-light)]">
              <tr>
                <th className="p-3 text-left">ID</th>
                <th className="p-3 text-left">Estado</th>
                <th className="p-3 text-left">Tipo</th>
                <th className="p-3 text-left">Patente</th>
                <th className="p-3 text-left">Acciones</th>
              </tr>
            </thead>

            <tbody>
              {estacionamientos.map((e) => (
                <tr
                  key={e.id}
                  className="border-b border-[var(--bg-alt)] hover:bg-[#2d3748]"
                >
                  <td className="p-3">{e.id}</td>
                  <td className="p-3">{e.estado}</td>
                  <td className="p-3">{e.tipo}</td>
                  <td className="p-3">{e.patente}</td>
                  <td className="p-3 flex gap-3">
                    <Link
                      href={`/estacionamientos/editar/${e.id}`}
                      className="button"
                    >
                      Editar
                    </Link>

                    <button
                      onClick={() => eliminarEstacionamientoHandler(e.id)}
                      className="button button-danger"
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
