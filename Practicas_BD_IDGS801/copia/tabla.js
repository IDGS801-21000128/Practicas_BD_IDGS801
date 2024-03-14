document.getElementById('send-signup').addEventListener('click', function(event) {

    var tamaño = document.querySelector('input[name="tamanio_pizza"]:checked').value;

    if (!tamaño) {
        alert('Por favor selecciona el tamaño de la pizza.');
        return;
    }

    var costoBase = 0;

    // Asignar costo base según el tamaño seleccionado
    if (tamaño === 'Chica') {
        costoBase = 40;
    } else if (tamaño === 'Mediana') {
        costoBase = 80;
    } else if (tamaño === 'Grande') {
        costoBase = 120;
    }

    var checkboxes = document.querySelectorAll('input[name="ingredientes"]:checked');

    if (checkboxes.length === 0) {
        alert('Por favor selecciona al menos un ingrediente.');
        return;
    }

var ingredientesSeleccionados = [];
checkboxes.forEach(function(checkbox) {
    ingredientesSeleccionados.push(checkbox.value);
});


    // Calcular costo de los ingredientes seleccionados
    var costoIngredientes = ingredientesSeleccionados.length * 10;

    var ingredienteTexto = ingredientesSeleccionados.join(', ');
    var cantidad = document.querySelector('input[name="cantidad"]').value;
    if (cantidad.trim() === '' || isNaN(cantidad) || parseInt(cantidad) <= 0) {
        alert('Por favor ingresa una cantidad válida.');
        return;
    }

    // Calcular subtotal sumando el costo base y el costo de los ingredientes
    var subtotal = (costoBase + costoIngredientes)*cantidad;

    var tabla = document.getElementById('tabla-dinamica').getElementsByTagName('tbody')[0];
    var fila = tabla.insertRow();

    var celda1 = fila.insertCell(0);
    var celda2 = fila.insertCell(1);
    var celda3 = fila.insertCell(2);
    var celda4 = fila.insertCell(3); 
    var celda5 = fila.insertCell(4); // Nueva celda para el botón "Quitar"

    celda1.innerHTML = tamaño;
    celda2.innerHTML = ingredienteTexto;
    celda3.innerHTML = cantidad;
    celda4.innerHTML = subtotal;
    celda5.innerHTML = '<button class="btn btn-danger quitar-fila">Quitar</button>'; // Botón "Quitar"

    document.querySelector('input[name="cantidad"]').value = '';
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = false;
    });

});

document.addEventListener("DOMContentLoaded", function() {
    var tabla = document.getElementById('tabla-dinamica');
    var filas = tabla.getElementsByTagName('tr');

    for (var i = 0; i < filas.length; i++) {
        filas[i].addEventListener('click', function() {
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
            } else {
                var filasSeleccionadas = tabla.querySelectorAll('tr.selected');
                filasSeleccionadas.forEach(function(fila) {
                    fila.classList.remove('selected');
                });
                this.classList.add('selected');
            }
        });
    }

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('quitar-fila')) {
            var filaSeleccionada = event.target.parentNode.parentNode; // Fila a la que pertenece el botón "Quitar"
            filaSeleccionada.remove();
        }
    });

});

document.getElementById('terminar-btn').addEventListener('click', function(event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente

    // Recopilar datos de nombre, domicilio y teléfono
    var nombre = document.getElementById('nombre').value;
    var direccion = document.getElementById('direccion').value;
    var telefono = document.getElementById('telefono').value;
    var fecha = document.getElementById('fecha').value;

    // Validar campos obligatorios
    if (nombre === '') {
        alert('Por favor ingresa tu nombre.');
        return;
    }
    if (direccion === '') {
        alert('Por favor ingresa tu dirección.');
        return;
    }
    if (telefono === '') {
        alert('Por favor ingresa tu número de teléfono.');
        return;
    }
    if (fecha === '') {
        alert('Por favor ingresa tu número de teléfono.');
        return;
    }

    // Recopilar datos de la tabla
    var tableRows = document.querySelectorAll('#tabla-dinamica tbody tr');
    var data = [];

    tableRows.forEach(function(row) {
        var rowData = {
            tamaño: row.cells[0].textContent,
            ingredientes: row.cells[1].textContent,
            cantidad: row.cells[2].textContent,
            subtotal: row.cells[3].textContent
        };
        data.push(rowData);
    });

    var postData = {
        nombre: nombre,
        direccion: direccion,
        telefono: telefono,
        fecha: fecha,
        pedidos: data
    };

    // Enviar los datos al servidor Flask
    fetch('/procesar_compra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
    })
    .then(response => {
        document.getElementById('tabla-dinamica').innerHTML = "<thead><tr><th style='background-color: lightblue;'>Tamaño</th><th style='background-color: lightblue;'>Ingredientes</th><th style='background-color: lightblue;'>Cantidad</th><th style='background-color: lightblue;'>Subtotal</th><th style='background-color: lightblue;'>Acción</th></tr></thead><tbody></tbody>";
        
    })
    .catch(error => {
        // Manejar errores si es necesario
    });
});




/*document.getElementById('buscar').addEventListener('click', function() {
    var fecha = document.getElementById('fechaInput').value;
    var filtro = document.querySelector('input[name="filtro"]:checked').value;
    
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/buscar?fecha=' + fecha + '&filtro=' + filtro, true);
    
    xhr.onload = function() {
        if (xhr.status === 200) {
            var datos = JSON.parse(xhr.responseText);
            var tabla = document.getElementById('tabla-consulta').getElementsByTagName('tbody')[0];
            tabla.innerHTML = ''; // Limpiar contenido actual de la tabla

            datos.forEach(function(registro) {
                var fila = tabla.insertRow();
                var celdaNombre = fila.insertCell(0);
                var celdaTotal = fila.insertCell(1);
                
                celdaNombre.innerHTML = registro.nombre;
                celdaTotal.innerHTML = registro.total;
            });
        }
    };
    
    xhr.send();
});*/

document.getElementById('filtrarMes').addEventListener('click', function(event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente
    var mesSeleccionado = document.getElementById('mesesDropdown').value;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_mes?mes=' + mesSeleccionado, true);
    
    xhr.onload = function() {
        var tabla = document.getElementById('tabla-consulta').getElementsByTagName('tbody')[0];
        tabla.innerHTML = '';
        if (xhr.status === 200) {
            var datos = JSON.parse(xhr.responseText);
            datos.forEach(function(registro) {
                var fila = tabla.insertRow();
                var celdaNombre = fila.insertCell(0);
                var celdaTotal = fila.insertCell(1);
                
                celdaNombre.innerHTML = registro.nombre;
                celdaTotal.innerHTML = registro.total;
            });
        }
    };
    xhr.send();
});

document.getElementById('filtrarDia').addEventListener('click', function(event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente
    var diaSeleccionado = document.getElementById('diasDropdown').value;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_dia?dia=' + diaSeleccionado, true);
    
    xhr.onload = function() {
        var tabla = document.getElementById('tabla-consulta').getElementsByTagName('tbody')[0];
        tabla.innerHTML = '';
        if (xhr.status === 200) {
            var datos = JSON.parse(xhr.responseText);
            datos.forEach(function(registro) {
                var fila = tabla.insertRow();
                var celdaNombre = fila.insertCell(0);
                var celdaTotal = fila.insertCell(1);
                
                celdaNombre.innerHTML = registro.nombre;
                celdaTotal.innerHTML = registro.total;
            });
        }
    };
    
    xhr.send();
});
