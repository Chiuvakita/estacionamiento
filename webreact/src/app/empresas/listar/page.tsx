"use client";
import { useState } from "react";
import Link from "next/link";
import NavbarAdmin from "@/components/NavbarAdmin";

interface Empresa {
  id: number;
  nombre: string;
  telefono: string;
  correo: string;
  direccion: string;
}

export default function EmpresasListarPage() {
  const [empresas, setEmpresas] = useState<Empresa[]>([
    // TEMPORAL — se reemplaza cuando llegue el backend
    {
      id: 1,
      nombre: "Empresa Demo",
      telefono: "+56912345678",
      correo: "demo@empresa.cl",
      direccion: "Calle Falsa 123",
    },
  ]);

  const [open, setOpen] = useState<number | null>(null);

  const toggle = (id: number) => {
    setOpen(open === id ? null : id);
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-4xl mx-auto p-6">
        <div className="mb-4">
          <Link
            href="/empresas/crear"
            className="px-4 py-2 rounded-[var(--radius)] bg-[var(--primary)] hover:bg-[var(--primary-dark)]"
          >
            Crear nueva empresa
          </Link>
        </div>

        <h1 className="text-2xl font-bold mb-6 text-center">
          Listado de Empresas
        </h1>

        <div className="space-y-3">
          {empresas.map((empresa) => (
            <div
              key={empresa.id}
              className="bg-[var(--bg-card)] rounded-[var(--radius)] shadow p-4"
            >
              <button
                onClick={() => toggle(empresa.id)}
                className="w-full flex justify-between items-center text-left"
              >
                <span className="flex items-center gap-2">
                  {open === empresa.id ? "▼" : "▶"}
                  <strong>{empresa.nombre}</strong>
                </span>

                <Link
                  href={`/empresas/${empresa.id}/sucursales/listar`}
                  className="px-3 py-1 rounded bg-[var(--primary)] hover:bg-[var(--primary-dark)]"
                >
                  Ver Sucursales
                </Link>

              </button>

              {open === empresa.id && (
                <div className="mt-3 border-t border-[var(--bg-alt)] pt-3">
                  <p>
                    <strong>Teléfono:</strong> {empresa.telefono}
                  </p>
                  <p>
                    <strong>Correo:</strong> {empresa.correo}
                  </p>
                  <p>
                    <strong>Dirección:</strong> {empresa.direccion}
                  </p>

                  <div className="flex gap-3 mt-3">
                    <Link
                      href={`/empresas/editar/${empresa.id}`}
                      className="px-3 py-2 rounded bg-[var(--primary)] hover:bg-[var(--primary-dark)]"
                    >
                      Editar
                    </Link>

                    <button className="px-3 py-2 rounded bg-[var(--danger)] hover:bg-[var(--danger-dark)]">
                      Eliminar
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
