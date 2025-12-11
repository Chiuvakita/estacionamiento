"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import NavbarAdmin from "@/components/NavbarAdmin";
import EmpresaForm from "@/components/EmpresaForm";

export default function EmpresaEditarPage() {
  const { id } = useParams(); // ← ID de la empresa desde la URL
  const router = useRouter();

  const [empresa, setEmpresa] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Simulación de API – reemplazar con fetch/axios cuando tengas backend
  useEffect(() => {
    // Simular fetch desde backend
    setTimeout(() => {
      setEmpresa({
        id,
        nombre: "Empresa de Prueba",
        telefono: "+56911112222",
        correo: "contacto@empresa.cl",
        direccion: "Av. Principal 123",
      });
      setLoading(false);
    }, 400);
  }, [id]);

  const handleSubmit = async (data: any) => {
    console.log("Datos actualizados:", data);

    alert("Empresa actualizada correctamente (simulación)");

    // Redirigir a listado
    router.push("/empresas/listar");
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

        <EmpresaForm initialData={empresa} onSubmit={handleSubmit} />

        <div className="mt-6 flex justify-center">
          <button
            onClick={() => router.push("/empresas/listar")}
            className="px-4 py-2 rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)]"
          >
            Volver
          </button>
        </div>
      </main>
    </div>
  );
}
