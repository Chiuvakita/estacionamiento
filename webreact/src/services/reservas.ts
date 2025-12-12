// src/services/reservas.ts
import api from "./api";

export interface Reserva {
  id: number;
  estacionamiento: number;
  vehiculo: number;
  fechaInicio: string;
  fechaTermino: string | null;
  tiempoRestante?: number;
}


export const listarReservas = async () => {
  const response = await api.get("reservas/");
  return response.data; // Filtrado ya hecho en el backend
};

export const terminarReserva = async (id: number) => {
  return api.post(`reservas/${id}/terminar/`);
};


export const listarEstacionamientosDisponibles = async () => {
  const { data } = await api.get("/estacionamientos/");

  // Solo disponibles
  return data.filter((e: any) => e.estado === "D");
};
