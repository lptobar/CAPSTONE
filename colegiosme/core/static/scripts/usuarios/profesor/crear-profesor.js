const formulario = document.querySelector('form');
const rut = formulario.querySelector('input[name=rut]');
const region = formulario.querySelector('select[name=region]');
const comuna = formulario.querySelector('select[name=comuna]');
const toastcontroller = document.querySelector('.toast-message');

rut.addEventListener('blur', async (ev) => {
    if (ev.target.value.length < 2 || ev.target.value === '') return;

    // FORMAT RUN
    let run = ev.target.value.replace(/[^0-9kK]/g, '')
    ev.target.value = run.replace(/(\w)(\w)$/, '$1-$2');
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
    
    try {
        const token = getCookie('csrftoken');

        const request = await fetch('/createTeacher/', { headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token }, method: 'POST', body: body });
        const response = await request.json();

        if (response.ok) {
            location.href = '/listar-usuarios/';
        } else {
            location.reload();
        }
    } catch (err) {
        console.log(err);
    }
});

function format(data) {
    data['rut'] = data['rut'].replace(/[^0-9kK]/g, '');

    data['p_nombre'] = data['nombres'].split(' ')[0];
    data['s_nombre'] = data['nombres'].split(' ').slice(1).join(' ');

    return JSON.stringify(data);
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