import api from "./api";

export interface SucursalPayload {
  nombreSucursal: string;
  direccion: string;
  numero: string;
  cantidadEstacionamiento: number;
}


export const crearSucursal = async (
  empresaID: number,
  data: any
) => {
  const payload = {
    ...data,
    empresa: empresaID, 
  };

  return (await api.post("/sucursales/", payload)).data;
};


export const listarSucursalesPorEmpresa = async (empresaID: number) => {
  const res = await api.get("/sucursales/", {
    params: { empresa: empresaID },
  });

  // Ajusta según tu response
  return res.data;
};

export const obtenerSucursal = async (id: number) => {
  const res = await api.get(`/sucursales/${id}/`);
  return res.data;
};

export const actualizarSucursal = async (id: number, data: any) => {
  const res = await api.put(`/sucursales/${id}/`, data);
  return res.data;
};

export const eliminarSucursal = async (id: number) => {
  const res = await api.delete(`/sucursales/${id}/`);
  return res.data;
};