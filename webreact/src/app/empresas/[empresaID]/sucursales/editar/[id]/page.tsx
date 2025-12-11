"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import NavbarAdmin from "@/components/NavbarAdmin";
import SucursalForm from "@/components/sucursaleFrom";

export default function EditarSucursalPage() {
  const { empresaID, id } = useParams(); // 👈 OJO: empresaID con ID mayúscula
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulación de carga desde API
    console.log("Cargando sucursal", id, "de empresa", empresaID);

    setTimeout(() => {
      setData({
        nombreSucursal: "Sucursal Centro",
        direccion: "Av. Principal 123",
        numero: "+56911112222",
        cantidadEstacionamiento: 12,
      });
      setLoading(false);
    }, 300);
  }, [empresaID, id]);

  const handleUpdate = (formData: any) => {
    console.log("Actualizar sucursal", id, "de empresa", empresaID, formData);

    // Más adelante:
    // axios.put(`/api/empresas/${empresaID}/sucursales/${id}/`, formData);

    alert("Sucursal actualizada (simulación)");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
        <NavbarAdmin />
        <div className="text-center mt-20">Cargando datos...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarAdmin />

      <main className="max-w-3xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 text-center">
          Editar Sucursal
        </h1>

        <div
          className="p-6 rounded-[var(--radius)] shadow"
          style={{ background: "var(--bg-card)" }}
        >
          <SucursalForm initialData={data} onSubmit={handleUpdate} isEdit={true} />
        </div>
      </main>
    </div>
  );
}
