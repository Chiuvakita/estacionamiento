// ahora importai la instancia que hiciste

import api from "../lib/api"; //asi


// ahora haci los get completando las rutas de la api asi como /usuarios

export const listarUsuarios = async () => { // usai el async como no es instantaneo y asi esperas con el await
    const response = await api.get("/usuarios/"); //asi
    return response.data;
};