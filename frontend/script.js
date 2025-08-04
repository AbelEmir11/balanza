// URL de tu API - cambia esto cuando hagas deployment
const API_URL = 'https://balanza-yg8u.onrender.com';

// Elementos del DOM
const form = document.getElementById('balanzaForm');
const resultadoDiv = document.getElementById('resultado');
const errorDiv = document.getElementById('error');
const calcularBtn = document.getElementById('calcularBtn');
const btnText = document.getElementById('btnText');
const spinner = document.getElementById('spinner');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    form.addEventListener('submit', handleSubmit);
    document.getElementById('nuevaConsulta').addEventListener('click', resetForm);
    document.getElementById('cerrarError').addEventListener('click', hideError);
});

// Función principal para manejar el envío del formulario
async function handleSubmit(e) {
    e.preventDefault();
    
    // Obtener datos del formulario
    const formData = new FormData(form);
    const userData = {
        sexo: formData.get('sexo'),
        edad: parseInt(formData.get('edad')),
        altura: parseFloat(formData.get('altura')),
        peso: parseFloat(formData.get('peso'))
    };

    // Validaciones básicas
    if (!validateData(userData)) {
        return;
    }

    // Mostrar estado de carga
    showLoading();

    try {
        // Hacer request a la API
        const response = await fetch(`${API_URL}/balanza`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error en el servidor');
        }

        const result = await response.json();
        showResult(result);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// Validaciones del lado del cliente
function validateData(data) {
    if (!data.sexo) {
        showError('Por favor selecciona tu género');
        return false;
    }

    if (data.edad < 1 || data.edad > 120) {
        showError('La edad debe estar entre 1 y 120 años');
        return false;
    }

    if (data.altura < 0.5 || data.altura > 3.0) {
        showError('La altura debe estar entre 0.5 y 3.0 metros');
        return false;
    }

    if (data.peso < 10 || data.peso > 500) {
        showError('El peso debe estar entre 10 y 500 kg');
        return false;
    }

    return true;
}

// Mostrar estado de carga
function showLoading() {
    calcularBtn.disabled = true;
    btnText.classList.add('hidden');
    spinner.classList.remove('hidden');
    hideError();
    hideResult();
}

// Ocultar estado de carga
function hideLoading() {
    calcularBtn.disabled = false;
    btnText.classList.remove('hidden');
    spinner.classList.add('hidden');
}

// Mostrar resultado
function showResult(data) {
    // Llenar los datos
    document.getElementById('imcValor').textContent = data.imc;
    document.getElementById('imcCategoria').textContent = data.categoria_imc;
    document.getElementById('generacionValor').textContent = data.generacion;
    document.getElementById('memeContenido').textContent = data.meme;
    document.getElementById('cancionContenido').textContent = data.cancion;
    document.getElementById('mensajeMotivacional').textContent = data.mensaje_motivacional;

    // Mostrar el resultado con animación
    hideError();
    resultadoDiv.classList.remove('hidden');
    
    // Scroll suave hacia el resultado
    setTimeout(() => {
        resultadoDiv.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

// Mostrar error
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorDiv.classList.remove('hidden');
    hideResult();
    
    // Scroll hacia el error
    setTimeout(() => {
        errorDiv.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

// Ocultar error
function hideError() {
    errorDiv.classList.add('hidden');
}

// Ocultar resultado
function hideResult() {
    resultadoDiv.classList.add('hidden');
}

// Reset del formulario
function resetForm() {
    form.reset();
    hideResult();
    hideError();
    
    // Scroll hacia arriba
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Función para testing - puedes usarla en la consola del navegador
function testAPI() {
    const testData = {
        sexo: "masculino",
        edad: 25,
        altura: 1.75,
        peso: 70
    };
    
    fetch(`${API_URL}/balanza`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(testData)
    })
    .then(response => response.json())
    .then(data => console.log('Test result:', data))
    .catch(error => console.error('Test error:', error));
}

// Agregar algunos efectos visuales extra
document.addEventListener('DOMContentLoaded', function() {
    // Efecto de aparición gradual
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s';
        document.body.style.opacity = '1';
    }, 100);
});