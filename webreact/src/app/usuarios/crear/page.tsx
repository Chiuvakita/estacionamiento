"use client";

import NavbarAdmin from "@/components/NavbarAdmin";
import UsuarioForm from "@/components/UsuarioForm";

export default function CrearUsuarioPage() {
  const handleSubmit = (data: any) => {
    console.log("Crear usuario:", data);
    alert("Usuario creado (simulación)");
  };

  return (
    <>
      <NavbarAdmin />
      <main className="px-6 py-10 max-w-5xl mx-auto">
        <h1 className="text-center text-3xl font-bold mb-6">Crear Usuario</h1>

        <UsuarioForm
        initialData={null}
        onSubmit={handleSubmit}
        buttonText="Crear Usuario"
        cancelHref="/usuarios/listar"
        />
      </main>
    </>
  );
}
