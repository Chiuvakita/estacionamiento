// src/services/vehiculos.ts
import api from "./api";

export interface Vehiculo {
  id: number;
  patente: string;
  marca: string;
  modelo: string;
  tipo: string;
}

export const listarVehiculos = async (): Promise<Vehiculo[]> => {
  const { data } = await api.get("vehiculos/");
  return data;
};

export const obtenerVehiculo = async (id: string | number) => {
  const res = await api.get(`vehiculos/${id}/`);
  return res.data;
};

export const crearVehiculo = async (data: {
  patente: string;
  marca: string;
  modelo: string;
  tipo: string;
}) => {
  const res = await api.post("vehiculos/", data);
  return res.data;
};

export const editarVehiculo = async (
  id: string | number,
  data: {
    patente: string;
    marca: string;
    modelo: string;
    tipo: string;
  }
) => {
  const res = await api.put(`vehiculos/${id}/`, data);
  return res.data;
};

export const eliminarVehiculo = async (id: number) => {
  return (await api.delete(`vehiculos/${id}/`)).data;
};

export const eliminarTodosVehiculos = async () => {
  const res = await api.delete("vehiculos/purge/");
  return res.data;
};



