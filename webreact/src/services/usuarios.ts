import api from "./api";

/* =========================
   TIPOS
========================= */
export interface Usuario {
  rut: number;
  nombre: string;
  apellidoPaterno: string;
  apellidoMaterno: string;
  numeroTelefono: string;
  rol: "Administrador" | "Empleado" | "Cliente";
  discapacidad: boolean;
  nombreCompleto?: string;
}

/* =========================
   LISTAR USUARIOS
========================= */
export const listarUsuarios = async (): Promise<Usuario[]> => {
  const response = await api.get("/usuarios/");
  const data = response.data;

  if (data?.success && Array.isArray(data.usuarios)) {
    return data.usuarios;
  }

  return [];
};

/* =========================
   ELIMINAR USUARIO
========================= */
export const eliminarUsuario = async (rut: number) => {
  const response = await api.delete(`/usuarios/${rut}/`);
  return response.data;
};



/* =========================
   CREAR USUARIO
========================= */
export const crearUsuario = async (data: any) => {
  const payload = { ...data };
  delete payload.confirmarClave;

  const response = await api.post("/usuarios/", payload);
  return response.data;
};


/* =========================
   CREAR CLIENTE (REGISTRO)
========================= */
export const crearCliente = async (data: any) => {
  return api.post("/usuarios/registro/", data);
};