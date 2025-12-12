"use client";

import NavbarCliente from "@/components/NavbarCliente";
import VehiculoForm from "@/components/VehiculoForm";
import { editarVehiculo, obtenerVehiculo } from "@/services/vehiculos";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function EditarVehiculoPage() {
  const { id } = useParams();
  const router = useRouter();

  const [vehiculo, setVehiculo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  /* =========================
     CARGA INICIAL
  ========================= */
  useEffect(() => {
    const cargarVehiculo = async () => {
      try {
        const data = await obtenerVehiculo(id as string);
        setVehiculo(data);
      } catch (error) {
        console.error(error);
        alert("Error al cargar el vehículo");
      } finally {
        setLoading(false);
      }
    };

    cargarVehiculo();
  }, [id]);

  /* =========================
     GUARDAR
  ========================= */
  const handleUpdate = async (data: any) => {
    try {
      await editarVehiculo(id as string, data);
      alert("Vehículo actualizado correctamente");
      router.push("/vehiculos/listar");
    } catch (error) {
      console.error(error);
      alert("Error al actualizar vehículo");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[var(--bg)] text-[var(--text)] flex items-center justify-center">
        Cargando...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarCliente />

      <main className="max-w-3xl mx-auto p-8">
        <h1 className="text-3xl font-bold mb-6 text-center">
          Editar Vehículo #{id}
        </h1>

        {vehiculo && (
          <VehiculoForm
            initialData={vehiculo}
            onSubmit={handleUpdate}
          />
        )}
      </main>
    </div>
  );
}
