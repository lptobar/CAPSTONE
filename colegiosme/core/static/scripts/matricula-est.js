const formulario = document.querySelector('#matricula');
const rut = document.querySelector('input[name=rut]');
const region = document.querySelector('select[name=region]');
const comuna = document.querySelector('select[name=comuna]');
const toastcontroller = document.querySelector('.toast-message');

rut.addEventListener('blur', async (ev) => {
    if (ev.target.value.length < 2 || ev.target.value === '') return;

    // FORMAT RUN
    let run = ev.target.value.replace(/[^0-9kK]/g, '')
    ev.target.value = run.replace(/(\w)(\w)$/, '$1-$2');

    showMessage('Buscando informacion del alumno.');
    // GET INFO ABOUT PERSON
    try {
        const request = await fetch(`/getPerson/${run}`);
        const response = await request.json();

        if (!response['ok']) {
            showMessage('No se encontro informacion.', 4000);
            return;
        }

        showMessage('Se encontro informacion.', 4000)
        // FILL DATA IN FORM
        Object.entries(response['data']).map(entry => {
            const [key, val] = entry;

            const input = formulario.querySelector(`input[name=${key}]`);
            const select = formulario.querySelector(`select[name=${key}]`);


            if (input !== null) {
                input.value = val;
            }
            if (select !== null) {
                if (select.name === 'region') region.dispatchEvent(new Event('change'))
                if (select.name === 'comuna') setTimeout(() => select.value = val, 500)
                else select.value = val;
            }
        });
    } catch (err) {
        showMessage('Ha ocurrido un error interno.', 5000);
        console.log(err);
    }
});
region.addEventListener('change', async (ev) => {
    comuna.innerHTML = '<option value="" selected>Elija una opcion</option>'

    const request = await fetch('/static/environment/comunas.json');
    const response = await request.json();

    const comunas = response[ev.target.value];
    for (let data of comunas) {
        comuna.innerHTML += `<option value="${data.id}">${data.name}</option>`;
    }
});
formulario.addEventListener('submit', async (ev) => {
    ev.preventDefault();

    const query = formulario.querySelectorAll('input, select');
    let body = {};

    for (let data of query) {
        body[data.name] = data.value;
    }
    body = format(body);

    showMessage('Validando informacion, por favor espere...');
    try {
        const token = getCookie('csrftoken');

        const request = await fetch('/createMatriculaStudent/', { headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token }, method: 'POST', body: body });
        const response = await request.json();

        if (response.ok) {
            showMessage('Redirigiendo...');
            setTimeout(() => {
                location.href = `/matricula-pdr/${response.id_matricula}`
            }, 3000);
        } else {
            showMessage(response.msg, 4000);
        }
    } catch (err) {
        showMessage('Ha ocurrido un error interno.', 5000);
        console.log(err);
    }
});

function format(data) {
    data['rut'] = data['rut'].replace(/[^0-9kK]/g, '');

    data['p_nombre'] = data['nombres'].split(' ')[0];
    data['s_nombre'] = data['nombres'].split(' ').slice(1).join(' ');

    return JSON.stringify(data);
}
function formatResponse(data) {
    data['rut'] = `${data['run']}`.replace(/(\w)(\w)$/, '$1-$2');
    data['nombres'] = `${data['p_nombre']} ${data['s_nombre']}`;

    return data;
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