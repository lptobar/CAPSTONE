const formulario = document.querySelector('#matricula');
const toastcontroller = document.querySelector('.toast-message');
const matricula = document.currentScript.dataset;

window.onload = async () => {
    try {
        const request = await fetch(`/getStudentInfo/${matricula.id}`);
        const response = await request.json();

        if (Object.keys(response).length == 0) {
            return;
        }

        Object.entries(response).map(entry => {
            const [key, val] = entry;

            const input = formulario.querySelector(`input[name=${key}]`);
            const select = formulario.querySelector(`select[name=${key}]`);

            if (input !== null) {
                if (input.type === 'radio') {
                    if (key === 'pie' && !val) alternarAutorizaEvaluacion(true);

                    const checkbox = formulario.querySelector(`input[type=radio][name=${key}][value=${val}]`);
                    if (checkbox !== null) {
                        checkbox.checked = true;
                    }
                } else {
                    input.value = val;
                }
            }
            if (select !== null) {
                select.value = val;
            }
        });
    } catch (err) {
        console.log(err);
    }
};
 
formulario.addEventListener('submit', async (ev) => {
    ev.preventDefault();

    const query = formulario.querySelectorAll('input, select');
    let body = {};

    for (let data of query) {
        if (data.type == 'radio') {
            if (data.checked) {
                body[data.name] = data.value;
            }
        } else {
            body[data.name] = data.value;
        }
    }
    body = format(body);
    
    try {
        const token = getCookie('csrftoken');
        console.log(token);

        const request = await fetch(`/updateStudentInfo/${matricula.id}`, { headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token }, method: 'PUT', body: body });
        const response = await request.json();

        if (response.ok) {
            showMessage('Redirigiendo...');
            setTimeout(() => {
                location.href = `/matricula-pdr/${matricula.id}`
            }, 3000);
        }
    } catch (err) {
        showMessage('Ha ocurrido un error interno.', 5000);
        console.log(err);
    }
});
function alternarEtnia(mostrar) {
    const option = mostrar ? 'block' : 'none';
    const etnia = document.querySelector('#indiqueEtnia');

    etnia.style.display = option;
}
function alternarAutorizaEvaluacion(mostrar) {
    const option = mostrar ? 'block' : 'none';
    const autorizaEvaluacion = document.querySelector('#autorizaEvaluacion');

    autorizaEvaluacion.style.display = option;
}
function format(data) {
    data['estudiante_prioritario'] = data['estudiante_prioritario'] === 'true' ? true : false;
    data['pie'] = data['pie'] === 'true' ? true : false;
    data['evaluacion_profesional'] = (data['evaluacion_profesional'] === 'true' ? true : false) ?? false

    return JSON.stringify(data);
}
function showMessage(message, duration = 0) {
    toastcontroller.style.display = 'block';
    toastcontroller.innerHTML = message;

    if (duration > 0) {
        setTimeout(() => {
            toastcontroller.style.display = 'none';
            toastcontroller.innerHTML = '';
        }, duration);
    }
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}