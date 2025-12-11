"use client";

import { useState } from "react";
import Link from "next/link";

export default function UsuarioForm({ initialData, onSubmit, buttonText, cancelHref }: any) {

  const [form, setForm] = useState(
    initialData || {
      rut: "",
      nombre: "",
      apellidoPaterno: "",
      apellidoMaterno: "",
      numeroTelefono: "",
      rol: "Cliente",
      discapacidad: false,
      clave: "",
      confirmar_clave: "",
    }
  );

  const update = (field: string, value: any) => {
    setForm({ ...form, [field]: value });
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <div
      className="max-w-3xl mx-auto p-8 rounded-lg shadow-lg"
      style={{ background: "var(--bg-card)" }}
    >
      <h1 className="text-center text-2xl font-bold mb-6">{buttonText}</h1>

      <form onSubmit={handleSubmit}>

        {/* GRID DE 2 COLUMNAS */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">

          {/* RUT */}
          <div>
            <label className="font-semibold block mb-1">RUT</label>
            <input
              className="w-full input-estilo"
              value={form.rut}
              onChange={(e) => update("rut", e.target.value)}
              placeholder="12345678-9"
            />
          </div>

          {/* Nombre */}
          <div>
            <label className="font-semibold block mb-1">Nombre</label>
            <input
              className="w-full input-estilo"
              value={form.nombre}
              onChange={(e) => update("nombre", e.target.value)}
            />
          </div>

          {/* Apellido Paterno */}
          <div>
            <label className="font-semibold block mb-1">Apellido Paterno</label>
            <input
              className="w-full input-estilo"
              value={form.apellidoPaterno}
              onChange={(e) => update("apellidoPaterno", e.target.value)}
            />
          </div>

          {/* Apellido Materno */}
          <div>
            <label className="font-semibold block mb-1">Apellido Materno</label>
            <input
              className="w-full input-estilo"
              value={form.apellidoMaterno}
              onChange={(e) => update("apellidoMaterno", e.target.value)}
            />
          </div>

          {/* Teléfono */}
          <div>
            <label className="font-semibold block mb-1">Teléfono</label>
            <input
              className="w-full input-estilo"
              value={form.numeroTelefono}
              onChange={(e) => update("numeroTelefono", e.target.value)}
              placeholder="+569XXXXXXX"
            />
          </div>

          {/* Rol */}
          <div>
            <label className="font-semibold block mb-1">Rol</label>
            <select
              className="w-full input-estilo"
              value={form.rol}
              onChange={(e) => update("rol", e.target.value)}
            >
              <option value="Administrador">Administrador</option>
              <option value="Cliente">Cliente</option>
            </select>
          </div>

          {/* Discapacidad */}
          <div className="flex items-center gap-2 mt-2">
            <input
              type="checkbox"
              checked={form.discapacidad}
              onChange={(e) => update("discapacidad", e.target.checked)}
            />
            <label className="font-semibold">Discapacidad</label>
          </div>

          {/* Clave */}
          <div>
            <label className="font-semibold block mb-1">Clave</label>
            <input
              type="password"
              className="w-full input-estilo"
              value={form.clave}
              onChange={(e) => update("clave", e.target.value)}
            />
          </div>

          {/* Confirmar clave */}
          <div>
            <label className="font-semibold block mb-1">Confirmar clave</label>
            <input
              type="password"
              className="w-full input-estilo"
              value={form.confirmar_clave}
              onChange={(e) => update("confirmar_clave", e.target.value)}
            />
          </div>

        </div>

        {/* Botones */}
        <div className="flex justify-center gap-4 mt-10">
          {cancelHref && (
            <Link
              href={cancelHref}
              className="button button-danger"
            >
              Cancelar
            </Link>
          )}

          <button
            type="submit"
            className="button"
          >
            {buttonText}
          </button>
        </div>

      </form>
    </div>
  );
}
