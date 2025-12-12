import api from "@/services/api";

export interface Estacionamiento {
  id: number;
  estado: string;
  tipo: string;
  patente: string | null;
}

/* LISTAR */
export const listarEstacionamientos = async (): Promise<Estacionamiento[]> => {
  const res = await api.get("/estacionamientos/");
  return res.data;
};

/* ELIMINAR UNO */
export const eliminarEstacionamiento = async (id: number) => {
  return await api.delete(`/estacionamientos/${id}/`);
};

/* ELIMINAR TODOS */
export const eliminarTodosEstacionamientos = async () => {
  return (await api.delete("estacionamientos/purge/")).data;
};



export const crearEstacionamiento = async (data: {
  estado: "D" | "O";
  tipo: "Normal" | "VIP" | "Discapacitado";
  patente: string;
}) => {
  return (await api.post("estacionamientos/", data)).data;
};

export const crearEstacionamientoMasivo = async (data: {
  cantidad: number;
  tipo: "Normal" | "VIP" | "Discapacitado";
}) => {
  return (await api.post("estacionamientos/bulk/", data)).data;
};
