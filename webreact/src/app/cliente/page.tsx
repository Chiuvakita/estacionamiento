"use client";

import Link from "next/link";
import { useState } from "react";

export default function HomeCliente() {
  // Simulamos el usuario mientras no llega backend
  const [user] = useState({
    nombreCompleto: "Usuario de Prueba",
  });

  return (
    <main className="p-6 min-h-screen bg-[var(--bg)] text-[var(--text)]">
      {/* Título */}
      <h1 className="text-3xl font-bold mb-4">
        Bienvenido, {user.nombreCompleto}
      </h1>

      {/* Descripción */}
      <p className="text-[var(--text-light)] mb-8">
        Desde aquí puedes gestionar tus reservas de estacionamiento.
      </p>

      {/* Botón */}
      <Link
        href="/reservas/listar"
        className="inline-block px-6 py-3 mt-4 font-semibold rounded-md 
                   bg-[var(--primary)] hover:bg-[var(--primary-dark)] 
                   transition-transform hover:scale-[1.03]"
      >
        Ver mis reservas
      </Link>
    </main>
  );
}
