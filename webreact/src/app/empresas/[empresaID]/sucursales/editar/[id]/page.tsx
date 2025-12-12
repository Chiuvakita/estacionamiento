"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import NavbarAdmin from "@/components/NavbarAdmin";
import SucursalForm from "@/components/sucursaleFrom";
import { obtenerSucursal, actualizarSucursal } from "@/services/sucursales";
import { useRouter } from "next/navigation";

export default function EditarSucursalPage() {
  const { empresaID, id } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    if (!id) return;

    setLoading(true);

    obtenerSucursal(Number(id))
      .then((res) => {
        setData(res);
      })
      .catch((err) => {
        console.error("Error cargando sucursal", err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [id]);


  const handleUpdate = async (formData: any) => {
    try {
      await actualizarSucursal(Number(id), {
        ...formData,
        empresa: Number(empresaID),
      });

      alert("Sucursal actualizada correctamente");

      // ⬅️ VOLVER AL LISTADO DE SUCURSALES
      router.push(`/empresas/${empresaID}/sucursales/listar`);

    } catch (error) {
      console.error("Error actualizando sucursal", error);
      alert("Error al actualizar la sucursal");
    }
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
