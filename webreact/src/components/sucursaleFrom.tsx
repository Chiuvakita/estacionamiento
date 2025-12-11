"use client";

import { useState } from "react";

interface SucursalFormProps {
  initialData?: {
    nombreSucursal?: string;
    direccion?: string;
    numero?: string;
    cantidadEstacionamiento?: number;
  };
  onSubmit: (data: any) => void;
  isEdit?: boolean;
}

export default function SucursalForm({
  initialData,
  onSubmit,
  isEdit = false,
}: SucursalFormProps) {
  const [form, setForm] = useState({
    nombreSucursal: initialData?.nombreSucursal || "",
    direccion: initialData?.direccion || "",
    numero: initialData?.numero || "",
    cantidadEstacionamiento: initialData?.cantidadEstacionamiento || "",
  });

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const validarTelefono = (val: string) => /^\+569\d{8}$/.test(val);
  const validarCantidad = (val: string) => /^[1-9]\d*$/.test(val);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validarCantidad(form.cantidadEstacionamiento.toString())) {
      alert("La cantidad debe ser un número positivo.");
      return;
    }

    if (!validarTelefono(form.numero)) {
      alert("El número debe tener formato +569XXXXXXXX");
      return;
    }

    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-6">

      {/* Nombre */}
      <div>
        <label className="font-semibold block mb-1">Nombre de Sucursal</label>
        <input
          type="text"
          name="nombreSucursal"
          value={form.nombreSucursal}
          onChange={handleChange}
          className="w-full px-4 py-2 bg-[var(--bg-card)] border border-[var(--bg-alt)]
                     rounded-md focus:border-[var(--primary)] focus:ring-[var(--primary)]"
        />
      </div>

      {/* Dirección */}
      <div>
        <label className="font-semibold block mb-1">Dirección</label>
        <input
          type="text"
          name="direccion"
          value={form.direccion}
          onChange={handleChange}
          className="w-full px-4 py-2 bg-[var(--bg-card)] border border-[var(--bg-alt)]
                     rounded-md focus:border-[var(--primary)] focus:ring-[var(--primary)]"
        />
      </div>

      {/* Número */}
      <div>
        <label className="font-semibold block mb-1">Número Telefónico</label>
        <input
          type="text"
          name="numero"
          placeholder="+569XXXXXXXX"
          value={form.numero}
          onChange={handleChange}
          className="w-full px-4 py-2 bg-[var(--bg-card)] border border-[var(--bg-alt)]
                     rounded-md focus:border-[var(--primary)] focus:ring-[var(--primary)]"
        />
      </div>

      {/* Cantidad */}
      <div>
        <label className="font-semibold block mb-1">Cantidad de Estacionamientos</label>
        <input
          type="number"
          name="cantidadEstacionamiento"
          value={form.cantidadEstacionamiento}
          onChange={handleChange}
          className="w-full px-4 py-2 bg-[var(--bg-card)] border border-[var(--bg-alt)]
                     rounded-md focus:border-[var(--primary)] focus:ring-[var(--primary)]"
        />
      </div>

      <div className="flex gap-3 mt-4">

        <button
          type="submit"
          className="px-6 py-3 bg-[var(--success)] hover:bg-[var(--success-dark)]
                     rounded-md font-semibold"
        >
          {isEdit ? "Guardar Cambios" : "Crear Sucursal"}
        </button>

        <a
          href="/empresas/listar"
          className="px-6 py-3 bg-[var(--danger)] hover:bg-[var(--danger-dark)]
                     rounded-md font-semibold"
        >
          Cancelar
        </a>

      </div>
    </form>
  );
}
