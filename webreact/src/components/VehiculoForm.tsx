"use client";

import { useState } from "react";
import Link from "next/link";

interface Props {
  onSubmit: (data: any) => void;
  initialData?: any;
}

export default function VehiculoForm({ onSubmit, initialData }: Props) {
  const [patente, setPatente] = useState(initialData?.patente || "");
  const [marca, setMarca] = useState(initialData?.marca || "");
  const [modelo, setModelo] = useState(initialData?.modelo || "");
  const [tipo, setTipo] = useState(initialData?.tipo || "");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    /* =====================
       VALIDACIONES FRONT
    ===================== */
    if (!patente.trim()) {
      alert("Patente requerida");
      return;
    }

    if (patente.trim().length !== 6) {
      alert("Patente debe tener 6 caracteres");
      return;
    }

    if (!marca.trim()) {
      alert("Marca requerida");
      return;
    }

    if (marca.length > 50) {
      alert("Marca: máximo 50 caracteres");
      return;
    }

    if (!modelo.trim()) {
      alert("Modelo requerido");
      return;
    }

    if (modelo.length > 50) {
      alert("Modelo: máximo 50 caracteres");
      return;
    }

    if (!tipo.trim()) {
      alert("Tipo requerido");
      return;
    }

    if (tipo.length > 50) {
      alert("Tipo: máximo 50 caracteres");
      return;
    }

    onSubmit({
      patente: patente.toUpperCase(),
      marca: marca.trim(),
      modelo: modelo.trim(),
      tipo: tipo.trim(),
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-6 p-6 rounded-[var(--radius)] shadow"
      style={{ background: "var(--bg-card)" }}
    >
      {/* PATENTE */}
      <div>
        <label className="block font-semibold mb-1">Patente</label>
        <input
          type="text"
          value={patente}
          onChange={(e) => setPatente(e.target.value.toUpperCase())}
          maxLength={6}
          placeholder="ABC123"
          className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)]"
        />
      </div>

      {/* MARCA */}
      <div>
        <label className="block font-semibold mb-1">Marca</label>
        <input
          type="text"
          value={marca}
          onChange={(e) => setMarca(e.target.value)}
          className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)]"
        />
      </div>

      {/* MODELO */}
      <div>
        <label className="block font-semibold mb-1">Modelo</label>
        <input
          type="text"
          value={modelo}
          onChange={(e) => setModelo(e.target.value)}
          className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)]"
        />
      </div>

      {/* TIPO */}
      <div>
        <label className="block font-semibold mb-1">Tipo</label>
        <input
          type="text"
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
          className="w-full px-4 py-3 rounded-md bg-[var(--bg-alt)] border border-[var(--bg-alt)]"
        />
      </div>

      {/* BOTONES */}
      <div className="flex gap-4">
        <button
          type="submit"
          className="flex-1 py-3 rounded-md bg-[var(--primary)] font-semibold hover:bg-[var(--primary-dark)]"
        >
          Guardar
        </button>

        <Link
          href="/vehiculos/listar"
          className="flex-1 py-3 rounded-md text-center bg-[var(--danger)] font-semibold hover:bg-[var(--danger-dark)]"
        >
          Cancelar
        </Link>
      </div>
    </form>
  );
}
