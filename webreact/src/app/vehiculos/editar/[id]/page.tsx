"use client";

import NavbarCliente from "@/components/NavbarCliente";
import Link from "next/link";
import { useParams } from "next/navigation";

export default function EditarVehiculoPage() {
  const { id } = useParams();

  const handleSave = (e: any) => {
    e.preventDefault();
    alert(`Vehículo ${id} actualizado (simulación)`);
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarCliente />

      <main className="max-w-xl mx-auto p-8">
        <h1 className="text-3xl font-bold mb-6 text-center">
          Editar Vehículo #{id}
        </h1>

        <div
          className="p-6 rounded-[var(--radius)] shadow-lg"
          style={{ background: "var(--bg-card)" }}
        >
          <form onSubmit={handleSave} className="space-y-4">

            {/* Patente */}
            <div>
              <label className="block mb-1 text-[var(--text-light)]">Patente</label>
              <input type="text" className="w-full p-3 rounded-md bg-[var(--bg-alt)]" defaultValue="AAA111" />
            </div>

            {/* Marca */}
            <div>
              <label className="block mb-1 text-[var(--text-light)]">Marca</label>
              <input type="text" className="w-full p-3 rounded-md bg-[var(--bg-alt)]" defaultValue="Toyota" />
            </div>

            {/* Modelo */}
            <div>
              <label className="block mb-1 text-[var(--text-light)]">Modelo</label>
              <input type="text" className="w-full p-3 rounded-md bg-[var(--bg-alt)]" defaultValue="Corolla" />
            </div>

            {/* Tipo */}
            <div>
              <label className="block mb-1 text-[var(--text-light)]">Tipo</label>
              <select className="w-full p-3 rounded-md bg-[var(--bg-alt)]">
                <option>Auto</option>
                <option>Moto</option>
                <option>Camioneta</option>
              </select>
            </div>

            {/* Botones */}
            <div className="flex gap-3">
              <button
                type="submit"
                className="flex-1 py-3 rounded-md bg-[var(--success)] hover:bg-[var(--success-dark)]"
              >
                Guardar Cambios
              </button>

              <Link
                href="/vehiculos/listar"
                className="flex-1 py-3 text-center rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)]"
              >
                Cancelar
              </Link>
            </div>

          </form>
        </div>
      </main>
    </div>
  );
}
