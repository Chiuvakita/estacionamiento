// aca usas el axios o conocido como el axe lshfs para las http

import axios from "axios"; // asi 

//creai la instancia de axios pa no repetir el codigo en las llamadas

const api = axios.create([{
    urlBase: "http://localhost:8000/api",// le metes la url de la api para que no la tengai que poner a cada rato
    headers: {
        "Content-Type": "application/json"
    },
}])

//ahora teni que pescar las peticiones antes de mandarlas como meterles un red antes de que se suelten 
//esto para pescar el token 
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
})

export default api