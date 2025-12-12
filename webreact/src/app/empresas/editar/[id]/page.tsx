"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import NavbarAdmin from "@/components/NavbarAdmin";
import EmpresaForm from "@/components/EmpresaForm";
import { obtenerEmpresa, editarEmpresa } from "@/services/empresas";

export default function EmpresaEditarPage() {
  const params = useParams();
  const id = Number(params.id);
  const router = useRouter();

  const [empresa, setEmpresa] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  /* CARGAR EMPRESA */
  useEffect(() => {
    const cargarEmpresa = async () => {
      try {
        const data = await obtenerEmpresa(id);
        setEmpresa(data);
      } catch (error) {
        alert("Error al cargar la empresa");
      } finally {
        setLoading(false);
      }
    };

    if (id) cargarEmpresa();
  }, [id]);

  /* GUARDAR CAMBIOS */
  const handleSubmit = async (data: any) => {
    try {
      await editarEmpresa(id, data);
      router.push("/empresas/listar");
    } catch (error) {
      alert("Error al actualizar empresa");
      console.error(error);
    }
  };

  if (loading) {
    return (
      <div className="text-center text-[var(--text)] mt-20">
        Cargando datos de la empresa...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-2xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 text-center">
          Editar Empresa
        </h1>

        <EmpresaForm
          initialData={empresa}
          onSubmit={handleSubmit}
          isEdit
        />
      </main>
    </div>
  );
}
