// Obtener el formulario por su ID o cualquier otro selector
const form = document.getElementById('formulario');

// Agregar un controlador de eventos para el evento "submit" del formulario
form.addEventListener('submit', function (event) {
  event.preventDefault(); // Evita que el formulario se envíe de forma predeterminada

  // Recopilar los datos del formulario en un objeto JavaScript
  const dataToSend = {
    numero_recibo: form.querySelector('[name="Número_recibo"]').value,
    numero_cuenta: form.querySelector('[name="Número_cuenta"]').value,
    nombre_y_apellido_estudiante: form.querySelector('[name="nombre_y_apellido_estudiante"]').value,
    dni: form.querySelector('[name="dni"]').value,
    fecha_nacimiento: form.querySelector('[name="fecha_nacimiento"]').value,
    edad:form.querySelector('[name="edad"]').value,
    direccion:form.querySelector('[name="dirección"]').value,
    barrio:form.querySelector('[name="barrio"]').value,
    celular:form.querySelector('[name="celular"]').value,
    telefono:form.querySelector('[name="teléfono"]').value,
    mail:form.querySelector('[name="mail"]').value,
    curso:form.querySelector('[name="curso"]').value,
    dia:form.querySelector('[name="día"]').value,
    hora_de_curso:form.querySelector('[name="hora_de_curso"]').value,
    fecha_de_inicio:form.querySelector('[name="fecha_de_inicio"]').value,
    vendedor:form.querySelector('[name="vendedor"]').value,
    ciudad:form.querySelector('[name="ciudad"]').value,
    plan:form.querySelector('[name="plan"]').value,
    forma_de_pago:form.querySelector('[name="forma_de_pago"]').value,
    valor_cuotas:form.querySelector('[name="valor_cuotas"]').value,
    cantidad_de_cuotas:form.querySelector('[name="cantidad_de_cuotas"]').value,
    valor_certificado:form.querySelector('[name="valor_certificado"]').value,
    abona_matricula:form.querySelector('[name="abona_matricula"]').value,
    abona_cuota_1:form.querySelector('[name="abona_cuota_1"]').value,
    abona_cuota_2:form.querySelector('[name="abona_cuota_2"]').value,
    abona_certificado:form.querySelector('[name="abona_certificado"]').value,

    // ...otros campos de datos
  };

  // Realizar una solicitud POST con fetch
  fetch('/registrar_estudiantes', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(dataToSend),
  })
    .then(response => response.json())
    .then(data => {
      // Hacer algo con la respuesta del servidor
    })
    .catch(error => {
      console.error('Error:', error);
    });
});
