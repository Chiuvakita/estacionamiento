"use client";

import { useParams } from "next/navigation";
import NavbarAdmin from "@/components/NavbarAdmin";
import SucursalForm from "@/components/sucursaleFrom";

export default function CrearSucursalPage() {
  const { empresaId } = useParams();

  const handleCreate = (data: any) => {
    console.log("Crear sucursal para empresa:", empresaId, data);

    // Luego:
    // axios.post(`/api/empresas/${empresaId}/sucursales/`, data);

    alert("Sucursal creada (simulación)");
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-3xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 text-center">
          Crear Sucursal
        </h1>

        <div className="p-6 rounded-[var(--radius)] shadow" style={{ background: "var(--bg-card)" }}>
          <SucursalForm onSubmit={handleCreate} />
        </div>
      </main>
    </div>
  );
}
