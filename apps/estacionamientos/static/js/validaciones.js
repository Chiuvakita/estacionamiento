
const regexPatente = /^[A-Za-z0-9]{5,8}$/; 

// ===============================
// ESTACIONAMIENTO
// ===============================

function validarIngresoVehiculo(e) {
  const patente = document.querySelector("input[name='patente']").value.trim();
  const modo = document.getElementById("modo")?.value;
  const estSelect = document.getElementById("estacionamiento_id");

  if (!regexPatente.test(patente)) {
    alert("La patente debe tener entre 5 y 8 caracteres alfanuméricos.");
    e.preventDefault();
    return false;
  }

  if (modo === "especifico" && (!estSelect?.value || estSelect.value === "")) {
    alert("Debes seleccionar un espacio de estacionamiento.");
    e.preventDefault();
    return false;
  }
  return true;
}

function validarSalidaPatente(e) {
  const patente = document.querySelector("form[action$='salida_por_patente/'] input[name='patente']").value.trim();

  if (!regexPatente.test(patente)) {
    alert("Debes ingresar una patente válida para finalizar.");
    e.preventDefault();
    return false;
  }
  return confirm("¿Seguro que deseas marcar la salida de este vehículo?");
}

// ===============================
// RESERVAS
// ===============================

function validarReserva(e) {
  const patente = document.querySelector("input[name='patente']").value.trim();
  const fechaInput = document.querySelector("input[name='fecha_inicio']").value;
  const duracionEl = document.querySelector("[name='duracion']");
  const duracion = parseInt(duracionEl?.value);
  const est = document.querySelector("select[name='estacionamiento_id']").value;

  const regexPatente = /^[A-Za-z0-9]{5,8}$/;

  // Validar patente
  if (!regexPatente.test(patente)) {
    alert("Ingresa una patente válida (ej: ABC123).");
    e.preventDefault();
    return false;
  }

  // Validar fecha
  if (!fechaInput) {
    alert("Debes seleccionar una fecha de inicio.");
    e.preventDefault();
    return false;
  }

  const fechaInicio = new Date(fechaInput);
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);

  if (fechaInicio < hoy) {
    alert("La fecha no puede ser pasada.");
    e.preventDefault();
    return false;
  }
  if (fechaInicio.toDateString() === hoy.toDateString()) {
    alert("No puedes reservar para el mismo día.");
    e.preventDefault();
    return false;
  }

  // Validar duración
  if (isNaN(duracion) || duracion <= 0) {
    alert("La duración debe ser mayor a 0 horas.");
    e.preventDefault();
    return false;
  }
  if (duracion > 4) {
    alert("La duración máxima es de 4 horas.");
    e.preventDefault();
    return false;
  }

  // Validar estacionamiento
  if (!est) {
    alert("Debes elegir un estacionamiento.");
    e.preventDefault();
    return false;
  }

  return true;
}


// ===============================
// CRUD ESTACIONAMIENTOS
// ===============================

function validarEstacionamiento(e) {
  const tipo = document.querySelector("select[name='tipo']")?.value;

  if (!tipo) {
    alert("Debes seleccionar un tipo de estacionamiento.");
    e.preventDefault();
    return false;
  }
  return true;
}

// ===============================
// CONFIRMACIONES 
// ===============================

function confirmarAccion(e) {
  e.preventDefault(); 
  const form = e.target.closest("form");

  const espacioId = e.target.dataset.espacioId;

  let mensaje = "";
  if (espacioId) {
    mensaje = `¿Seguro que deseas eliminar el espacio #${espacioId}?`;
  } else {
    mensaje = "¿Seguro que deseas eliminar TODOS los estacionamientos?";
  }

  if (confirm(mensaje)) {
    form.submit(); 
  }
}


// ===============================
// TOGGLE SELECT 
// ===============================
function toggleSelect() {
  const selectDiv = document.getElementById("select-estacionamiento") || document.getElementById("selectEstacionamiento");
  const modo = document.getElementById("modo")?.value;
  if (modo === "especifico") {
    selectDiv.style.display = "block";
  } else {
    selectDiv.style.display = "none";
  }
}
