"use client";

import NavbarCliente from "@/components/NavbarCliente";
import Link from "next/link";

export default function TerminarReservaPage() {
  const handleFinish = () => {
    alert("Reserva finalizada (simulación)");
  };

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text)]">
      <NavbarCliente />

      <main className="max-w-xl mx-auto p-6 pt-10 text-center">
        <h1 className="text-3xl font-bold mb-6">Terminar Reserva</h1>

        <div
          className="p-8 rounded-[var(--radius)] shadow-lg"
          style={{ background: "var(--bg-card)" }}
        >
          <p className="mb-6">¿Estás seguro que deseas finalizar esta reserva?</p>

          <button
            onClick={handleFinish}
            className="w-full py-3 rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)] font-semibold transition"
          >
            Finalizar
          </button>

          <Link
            href="/reservas/listar"
            className="w-full block text-center py-3 mt-3 rounded-md bg-[var(--primary)] hover:bg-[var(--primary-dark)] font-semibold transition"
          >
            Cancelar
          </Link>
        </div>
      </main>
    </div>
  );
}
