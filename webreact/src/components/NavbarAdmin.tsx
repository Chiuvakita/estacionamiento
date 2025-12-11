"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

export default function NavbarAdmin() {
  const pathname = usePathname();
  const router = useRouter();

  const linkClass = (path: string) =>
    `px-4 py-2 rounded-md transition 
     ${
       pathname === path
         ? "bg-[var(--primary-dark)] text-white"
         : "text-[var(--text-light)] hover:bg-[var(--bg-alt)] hover:text-white"
     }`;

  const logout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <nav
      className="w-full flex items-center px-6 py-4 mb-6"
      style={{ background: "var(--bg-card)", boxShadow: "var(--shadow)" }}
    >
      {/* Enlaces */}
      <div className="flex gap-4">
        <Link href="/admin" className={linkClass("/admin")}>
          Inicio
        </Link>

        <Link href="/empresas/listar" className={linkClass("/empresas/listar")}>
          Empresas
        </Link>

        <Link href="/usuarios/listar" className={linkClass("/usuarios/listar")}>
          Usuarios
        </Link>

        <Link href="/estacionamientos/listar" className={linkClass("/estacionamientos/listar")}>
          Estacionamientos
        </Link>

        <Link href="/historial/listar" className={linkClass("/historial/listar")}>
          Historial
        </Link>
      </div>

      {/* Cerrar sesión */}
      <div className="ml-auto">
        <button
          onClick={logout}
          className="px-4 py-2 rounded-md bg-[var(--danger)] hover:bg-[var(--danger-dark)] text-white transition"
        >
          Cerrar Sesión
        </button>
      </div>
    </nav>
  );
}
