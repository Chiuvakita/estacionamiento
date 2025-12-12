// src/services/auth.ts
// LOGIN

import api from "./api";

export interface LoginResponse {
  success: boolean;
  token?: string;
  usuario?: {
    rut: number;
    rol: string;
    nombreCompleto: string;
  };
  detail?: string;
}

export const login = async (
  rut: string,
  clave: string
): Promise<LoginResponse> => {
  const response = await api.post("usuarios/login/", {
    username: rut,
    clave: clave,
  });

  return response.data;
};

// REGISTRO















