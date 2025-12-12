import api from "./api";

export interface Empresa {
  id: number;
  nombre: string;
  telefono: string;
  correo: string;
  direccion: string;
}

/* LISTAR */
export const listarEmpresas = async (): Promise<Empresa[]> => {
  const response = await api.get("/empresas/");
  return response.data.empresas ?? response.data;
};

/* OBTENER UNA */
export const obtenerEmpresa = async (id: number): Promise<Empresa> => {
  const response = await api.get(`/empresas/${id}/`);
  return response.data;
};

/* CREAR */
export const crearEmpresa = async (data: Omit<Empresa, "id">) => {
  return (await api.post("/empresas/", data)).data;
};

/* EDITAR */
export const editarEmpresa = async (id: number, data: Omit<Empresa, "id">) => {
  return (await api.put(`/empresas/${id}/`, data)).data;
};

/* ELIMINAR */
export const eliminarEmpresa = async (id: number) => {
  await api.delete(`/empresas/${id}/`);
};
