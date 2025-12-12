"use client";

import EmpresaForm from "@/components/EmpresaForm";
import NavbarAdmin from "@/components/NavbarAdmin";
import { crearEmpresa } from "@/services/empresas";
import { useRouter } from "next/navigation";

export default function CrearEmpresaPage() {
  const router = useRouter();

  const handleCreate = async (data: any) => {
    try {
      await crearEmpresa(data);
      router.push("/empresas/listar");
    } catch (error: any) {
      alert("Error al crear empresa");
      console.error(error);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-3xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 text-center">
          Crear Empresa
        </h1>

        <div
          className="p-6 rounded-[var(--radius)] shadow"
          style={{ background: "var(--bg-card)" }}
        >
          <EmpresaForm onSubmit={handleCreate} />
        </div>
      </main>
    </div>
  );
}
