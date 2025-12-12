"use client";

import NavbarAdmin from "@/components/NavbarAdmin";
import UsuarioForm from "@/components/UsuarioForm";
import { crearUsuario } from "@/services/usuarios";
import { useRouter } from "next/navigation";

/* =========================
   VALIDACIONES FRONTEND
========================= */
const validarUsuario = (data: any): string[] => {
  const errores: string[] = [];

  // RUT
  if (!data.rut) errores.push("El RUT es obligatorio.");
  if (!/^\d+$/.test(data.rut))
    errores.push("El RUT debe contener solo números.");
  if (data.rut.length < 7 || data.rut.length > 8)
    errores.push("El RUT debe tener entre 7 y 8 dígitos.");

  // Nombre
  if (!data.nombre || data.nombre.trim().length < 2)
    errores.push("El nombre debe tener al menos 2 caracteres.");

  // Apellidos
  if (!data.apellidoPaterno || data.apellidoPaterno.trim().length < 2)
    errores.push("El apellido paterno es obligatorio.");
  if (!data.apellidoMaterno || data.apellidoMaterno.trim().length < 2)
    errores.push("El apellido materno es obligatorio.");

  // Teléfono
  if (!data.numeroTelefono)
    errores.push("El número de teléfono es obligatorio.");
  if (!/^\+?\d{8,12}$/.test(data.numeroTelefono))
    errores.push("El número de teléfono debe tener entre 8 y 12 dígitos.");

  // Rol
  const rolesValidos = ["Administrador", "Empleado", "Cliente"];
  if (!rolesValidos.includes(data.rol))
    errores.push("Rol de usuario no válido.");

  // Clave
  if (data.clave) {
    if (data.clave.length < 8)
      errores.push("La contraseña debe tener al menos 8 caracteres.");
    if (!/[A-Za-z]/.test(data.clave))
      errores.push("La contraseña debe contener al menos una letra.");
    if (!/\d/.test(data.clave))
      errores.push("La contraseña debe contener al menos un número.");
    if (/\s/.test(data.clave))
      errores.push("La contraseña no puede contener espacios.");
  } else {
    errores.push("La contraseña es obligatoria.");
  }

  return errores;
};

/* =========================
   PAGE
========================= */
export default function CrearUsuarioPage() {
  const router = useRouter();

  const handleSubmit = async (data: any) => {
    // 🔍 VALIDAR ANTES DE ENVIAR
    const errores = validarUsuario(data);
    if (errores.length > 0) {
      alert(errores.join("\n"));
      return;
    }

    try {
      await crearUsuario(data);

      alert("Usuario creado correctamente");
      router.push("/usuarios/listar");

    } catch (error: any) {
      console.error(error);

      // SIN PERMISOS
      if (error.response?.status === 403) {
        alert(
          "No tienes permisos para crear usuarios.\n" +
          "Esta acción solo está permitida para administradores."
        );
        return;
      }

      //ERRORES DE VALIDACIÓN BACKEND (forms / serializer)
      if (error.response?.data) {
        const mensajes = Object.values(error.response.data)
          .flat()
          .join("\n");
        alert(mensajes);
        return;
      }

      alert("Error inesperado al crear usuario");
    }
  };

  return (
    <>
      <NavbarAdmin />

      <main className="px-6 py-10 max-w-5xl mx-auto">
        <h1 className="text-center text-3xl font-bold mb-6">
          Crear Usuario
        </h1>

        <UsuarioForm
          initialData={null}
          onSubmit={handleSubmit}
          buttonText="Crear Usuario"
          cancelHref="/usuarios/listar"
        />
      </main>
    </>
  );
}
