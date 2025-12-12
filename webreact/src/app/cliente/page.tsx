"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function HomeCliente() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const stored = localStorage.getItem("usuario");
    if (stored) {
      setUser(JSON.parse(stored));
    }
  }, []);

  if (!user) return null;

  return (
    <main className="p-6 min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <h1 className="text-3xl font-bold mb-4">
        Bienvenido, {user.nombreCompleto}
      </h1>

      <p className="text-[var(--text-light)] mb-8">
        Desde aquí puedes gestionar tus reservas de estacionamiento.
      </p>

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
