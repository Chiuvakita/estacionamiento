"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import NavbarAdmin from "@/components/NavbarAdmin";
import { listarUsuarios, eliminarUsuario } from "@/services/usuarios";

export default function UsuariosListarPage() {
  const [usuarios, setUsuarios] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const handleEliminar = async (rut: number) => {
    const confirmar = confirm(
      "¿Estás seguro de eliminar este usuario? Esta acción no se puede deshacer."
    );

    if (!confirmar) return;

    try {
      await eliminarUsuario(rut);

      // Actualizar tabla sin recargar
      setUsuarios((prev) => prev.filter((u) => u.rut !== rut));
    } catch (error) {
      console.error(error);
      alert("No tienes permiso para eliminar este usuario.");
    }
  };

  useEffect(() => {
    listarUsuarios()
      .then(setUsuarios)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-center mt-20">Cargando...</div>;
  }

  return (
    <>
      <NavbarAdmin />

      <main className="max-w-5xl mx-auto px-4 py-10">
        <h1 className="text-center text-3xl font-bold mb-6">Usuarios</h1>

        {/* CARD */}
        <div
          className="p-5 rounded-lg shadow-lg mb-6"
          style={{ background: "var(--bg-card)" }}
        >
          <Link
            href="/usuarios/crear"
            className="px-5 py-2 rounded-md text-white font-medium"
            style={{ background: "var(--primary)" }}
          >
            Crear Usuario
          </Link>
        </div>

        {/* TABLA */}
        <div className="overflow-hidden rounded-lg shadow-lg">
          <table
            className="w-full border-collapse"
            style={{ background: "var(--bg-card)" }}
          >
            <thead className="bg-[var(--bg-alt)]">
              <tr>
                {[
                  "Nombre",
                  "Apellido P.",
                  "Apellido M.",
                  "Teléfono",
                  "Rol",
                  "Discapacidad",
                  "Acciones",
                ].map((h) => (
                  <th
                    key={h}
                    className="p-3 text-left text-[var(--text-light)] font-semibold"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {usuarios.map((u) => (
                <tr
                  key={u.rut}
                  className="hover:bg-[#2d3748] transition"
                >
                  <td className="p-3">{u.nombre}</td>
                  <td className="p-3">{u.apellidoPaterno}</td>
                  <td className="p-3">{u.apellidoMaterno}</td>
                  <td className="p-3">{u.numeroTelefono}</td>
                  <td className="p-3">{u.rol}</td>
                  <td className="p-3">
                    {u.discapacidad ? "Sí" : "No"}
                  </td>

                  <td className="p-3 flex gap-3">
                    <Link
                      href={`/usuarios/editar/${u.rut}`}
                      className="px-4 py-2 rounded-md text-white"
                      style={{ background: "var(--primary)" }}
                    >
                      Editar
                    </Link>

                    <button
                      onClick={() => handleEliminar(u.rut)}
                      className="px-4 py-2 rounded-md text-white"
                      style={{ background: "var(--danger)" }}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}

              {usuarios.length === 0 && (
                <tr>
                  <td
                    colSpan={7}
                    className="text-center p-6 text-gray-400"
                  >
                    No hay usuarios registrados
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </main>
    </>
  );
}
