"use client";

import NavbarCliente from "@/components/NavbarCliente";
import VehiculoForm from "@/components/VehiculoForm";
import { crearVehiculo } from "@/services/vehiculos";
import { useRouter } from "next/navigation";

export default function CrearVehiculoPage() {
  const router = useRouter();

  const handleCreate = async (data: any) => {
    try {
      await crearVehiculo(data);
      alert("Vehículo creado correctamente");
      router.push("/vehiculos/listar");
    } catch (error: any) {
      console.error(error);
      alert("Error al crear vehículo");
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarCliente />

      <main className="max-w-3xl mx-auto p-8">
        <h1 className="text-3xl font-bold text-center mb-6">
          Crear Vehículo
        </h1>

        <VehiculoForm onSubmit={handleCreate} />
      </main>
    </div>
  );
}
