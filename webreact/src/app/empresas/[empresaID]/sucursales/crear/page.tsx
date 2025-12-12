"use client";

import { useParams, useRouter } from "next/navigation";
import NavbarAdmin from "@/components/NavbarAdmin";
import SucursalForm from "@/components/sucursaleFrom";
import { crearSucursal } from "@/services/sucursales";

export default function CrearSucursalPage() {
  const { empresaID } = useParams(); // ✅ NOMBRE CORRECTO
  const router = useRouter();

  const handleCreate = async (data: any) => {
    try {
      await crearSucursal(Number(empresaID), data);

      alert("Sucursal creada correctamente");
      router.push(`/empresas/${empresaID}/sucursales/listar`);
    } catch (error) {
      console.error(error);
      alert("Error al crear sucursal");
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-3xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 text-center">
          Crear Sucursal
        </h1>

        <div
          className="p-6 rounded-[var(--radius)] shadow"
          style={{ background: "var(--bg-card)" }}
        >
          <SucursalForm onSubmit={handleCreate} />
        </div>
      </main>
    </div>
  );
}
