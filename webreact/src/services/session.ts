export const getUsuario = () => {
  const u = localStorage.getItem("usuario");
  return u ? JSON.parse(u) : null;
};

export const isAuthenticated = () => {
  return !!localStorage.getItem("token");
};
