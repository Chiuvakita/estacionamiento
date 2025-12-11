"use client";

import { useState } from "react";

interface EmpresaFormProps {
  initialData?: {
    nombre?: string;
    telefono?: string;
    correo?: string;
    direccion?: string;
  };
  onSubmit: (data: any) => void;
  isEdit?: boolean;
}

export default function EmpresaForm({
  initialData,
  onSubmit,
  isEdit = false,
}: EmpresaFormProps) {
  const [form, setForm] = useState({
    nombre: initialData?.nombre || "",
    telefono: initialData?.telefono || "",
    correo: initialData?.correo || "",
    direccion: initialData?.direccion || "",
  });

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const validarTelefono = (num: string) => /^\+569\d{8}$/.test(num);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validarTelefono(form.telefono)) {
      alert("El número debe ser válido. Ejemplo: +569XXXXXXXX");
      return;
    }

    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-6">

      {/* Nombre */}
      <div>
        <label className="font-semibold block mb-1">Nombre de la empresa</label>
        <input
          type="text"
          name="nombre"
          value={form.nombre}
          onChange={handleChange}
          placeholder="Ej: Mi Empresa SPA"
          className="w-full px-4 py-2 bg-[var(--bg-card)] border border-[var(--bg-alt)]
                     rounded-md focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
        />
      </div>

      {/* Teléfono */}
      <div>
        <label className="font-semibold block mb-1">Teléfono</label>
        <input
          type="text"
          name="telefono"
          value={form.telefono}
          onChange={handleChange}
          placeholder="+569XXXXXXXX"
          className="w-full px-4 py-2 bg-[var(--bg-card)] border border-[var(--bg-alt)]
                     rounded-md focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
        />
      </div>

      {/* Correo */}
      <div>
        <label className="font-semibold block mb-1">Correo Electrónico</label>
        <input
          type="email"
          name="correo"
          value={form.correo}
          onChange={handleChange}
          placeholder="correo@empresa.cl"
          className="w-full px-4 py-2 bg-[var(--bg-card)] border border-[var(--bg-alt)]
                     rounded-md focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
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
          placeholder="Ej: Av. Siempre Viva 742"
          className="w-full px-4 py-2 bg-[var(--bg-card)] border border-[var(--bg-alt)]
                     rounded-md focus:border-[var(--primary)] focus:ring-[var(--primary)] focus:ring-2 outline-none"
        />
      </div>

      {/* Botones */}
      <div className="flex gap-3 mt-4">

        <button
          type="submit"
          className="px-6 py-3 rounded-md bg-[var(--success)] hover:bg-[var(--success-dark)]
                     font-semibold transition-transform hover:scale-[1.03]"
        >
          {isEdit ? "Guardar Cambios" : "Crear Empresa"}
        </button>

        <a
          href="/empresas/listar"
          className="px-6 py-3 rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)]
                     font-semibold transition-transform hover:scale-[1.03]"
        >
          Cancelar
        </a>
      </div>
    </form>
  );
}
