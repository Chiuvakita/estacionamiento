"use client";

import { useRouter } from "next/navigation";
import ClienteForm from "@/components/ClienteForm";
import { crearCliente } from "@/services/usuarios";

export default function RegistroPage() {
  const router = useRouter();

  const handleSubmit = async (data: any) => {
    try {
      await crearCliente(data);
      alert("Registro exitoso. Ahora puedes iniciar sesión.");
      router.push("/login");
    } catch (error: any) {
      const errors = error.response?.data?.errors;
      if (errors) {
        alert(Object.values(errors).flat().join("\n"));
        return;
      }
      alert("Error inesperado");
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center p-5">
      <ClienteForm onSubmit={handleSubmit} />
    </main>
  );
}
