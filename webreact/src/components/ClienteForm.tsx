"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

interface Props {
  onSubmit: (data: any) => void;
  buttonText?: string;
}

export default function ClienteForm({
  onSubmit,
  buttonText = "Registrarse",
}: Props) {

  const router = useRouter();

  const [form, setForm] = useState({
    rut: "",
    nombre: "",
    apellidoPaterno: "",
    apellidoMaterno: "",
    numeroTelefono: "",
    discapacidad: false,
    clave: "",
    confirmarClave: "",
    confirmar_clave: "", // requerido por backend actual
  });

  const update = (field: string, value: any) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <div
      className="max-w-3xl mx-auto p-8 rounded-lg shadow-lg"
      style={{ background: "var(--bg-card)" }}
    >
      <h1 className="text-center text-2xl font-bold mb-6">
        Registro de Cliente
      </h1>

      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">

          <div>
            <label className="font-semibold block mb-1">RUT</label>
            <input
              type="text"
              className="w-full input-estilo"
              value={form.rut}
              onChange={(e) => update("rut", e.target.value)}
            />
          </div>

          <div>
            <label className="font-semibold block mb-1">Nombre</label>
            <input
              className="w-full input-estilo"
              value={form.nombre}
              onChange={(e) => update("nombre", e.target.value)}
            />
          </div>

          <div>
            <label className="font-semibold block mb-1">Apellido Paterno</label>
            <input
              className="w-full input-estilo"
              value={form.apellidoPaterno}
              onChange={(e) => update("apellidoPaterno", e.target.value)}
            />
          </div>

          <div>
            <label className="font-semibold block mb-1">Apellido Materno</label>
            <input
              className="w-full input-estilo"
              value={form.apellidoMaterno}
              onChange={(e) => update("apellidoMaterno", e.target.value)}
            />
          </div>

          <div>
            <label className="font-semibold block mb-1">Teléfono</label>
            <input
              type="text"
              className="w-full input-estilo"
              value={form.numeroTelefono}
              onChange={(e) => update("numeroTelefono", e.target.value)}
            />
          </div>

          <div className="flex items-center gap-2 mt-2">
            <input
              type="checkbox"
              checked={form.discapacidad}
              onChange={(e) => update("discapacidad", e.target.checked)}
            />
            <label className="font-semibold">Discapacidad</label>
          </div>

          <div>
            <label className="font-semibold block mb-1">Contraseña</label>
            <input
              type="password"
              className="w-full input-estilo"
              value={form.clave}
              onChange={(e) => update("clave", e.target.value)}
            />
          </div>

          <div>
            <label className="font-semibold block mb-1">
              Confirmar contraseña
            </label>
            <input
              type="password"
              className="w-full input-estilo"
              value={form.confirmarClave}
              onChange={(e) => {
                update("confirmarClave", e.target.value);
                update("confirmar_clave", e.target.value);
              }}
            />
          </div>

        </div>

        {/* BOTONES */}
        <div className="flex justify-center gap-4 mt-10">
          <button type="submit" className="button">
            {buttonText}
          </button>

          <button
            type="button"
            className="button button-secondary"
            onClick={() => router.back()}
          >
            Ya tengo cuenta
          </button>
        </div>
      </form>
    </div>
  );
}
