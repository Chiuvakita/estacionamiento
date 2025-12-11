"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import NavbarAdmin from "@/components/NavbarAdmin";
import UsuarioForm from "@/components/UsuarioForm";

export default function EditarUsuarioPage() {
  const { rut } = useParams();
  const [usuario, setUsuario] = useState<any | null>(null);

  useEffect(() => {
    // Simulación – luego conectamos API real
    setUsuario({
      rut,
      nombre: "Carlos",
      apellidoPaterno: "Gomez",
      apellidoMaterno: "Lopez",
      numeroTelefono: "+56911112222",
      rol: "Administrador",
      discapacidad: false,
      clave: "",
      confirmar_clave: "",
    });
  }, [rut]);

  const handleSubmit = (data: any) => {
    alert("Usuario editado (simulación)");
    console.log("Editar usuario:", data);
  };

  if (!usuario) return <div className="text-center mt-20">Cargando...</div>;

  return (
    <>
      <NavbarAdmin />
      <main className="px-6 py-10 max-w-5xl mx-auto">
        <h1 className="text-center text-3xl font-bold mb-6">
          Editar Usuario
        </h1>

        <UsuarioForm
        initialData={usuario}
        onSubmit={handleSubmit}
        buttonText="Guardar Cambios"
        cancelHref="/usuarios/listar"
        />

      </main>
    </>
  );
}
