"use client";

import EmpresaForm from "@/components/EmpresaForm";
import NavbarAdmin from "@/components/NavbarAdmin";

export default function CrearEmpresaPage() {
  const handleCreate = (data: any) => {
    console.log("Datos enviados para crear empresa:", data);

    // Aquí después va:
    // axios.post("/api/empresas/", data)

    alert("Empresa creada (simulación)");
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
