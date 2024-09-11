const formulario = document.querySelectorAll('#matricula');
const rut = document.querySelectorAll('input[name=rut]');
const region = document.querySelectorAll('select[name=region]');
const comuna = document.querySelectorAll('select[name=comuna]');
const toastcontroller = document.querySelector('.toast-message');
const matricula = document.currentScript.dataset;

rut[0].addEventListener('blur', async (ev) => {
    if (ev.target.value.length < 2 || ev.target.value === '') return;

    // FORMAT RUN
    let run = ev.target.value.replace(/[^0-9kK]/g, '')
    ev.target.value = run.replace(/(\w)(\w)$/, '$1-$2');

    // GET INFO ABOUT PERSON
    try {
        showMessage('Buscando informacion...');

        const request = await fetch(`/getPerson/${run}`);
        const response = await request.json();
        
        if (!response['ok']) {
            showMessage('No se ha encontrado informacion.', 4000);
            return;
        }

        showMessage('Se ha encontrado informacion.', 4000);
        // FILL DATA IN FORM
        Object.entries(response['data']).map(entry => {
            const [key, val] = entry;
            const input = formulario[0].querySelector(`input[name=${key}]`);
            const select = formulario[0].querySelector(`select[name=${key}]`);

            if (input != null) {
                if (input.type === 'radio') {
                    if (key === 'vive_con_alumno') alternarDireccionPdr(!val);

                    const checkbox = formulario[0].querySelector(`input[name=${key}][value=${val}]`);
                    checkbox.checked = true;
                } else {
                    input.value = val;
                }
            }
            if (select != null) {
                if (select.name == 'region') region[0].dispatchEvent(new Event('change'));
                if (select.name == 'comuna') setTimeout(() => select.value = val, 500)
                select.value = val;
            }
        });
    } catch (err) {
        showMessage('Ha ocurrido un error interno.', 5000);
        console.log(err);
    }
});
rut[1].addEventListener('blur', async (ev) => {
    if (ev.target.value.length < 2 || ev.target.value === '') return;

    // FORMAT RUN
    let run = ev.target.value.replace(/[^0-9kK]/g, '')
    ev.target.value = run.replace(/(\w)(\w)$/, '$1-$2');

    // GET INFO ABOUT PERSON
    try {
        const request = await fetch(`/getPerson/${run}`);
        const response = await request.json();

        if (!response['ok']) {
            showMessage('No se ha encontrado informacion.', 4000);
            return;
        }

        showMessage('Se ha encontrado informacion.', 4000);
        // FILL DATA IN FORM
        Object.entries(response['data']).map(entry => {
            const [key, val] = entry;
            const input = formulario[1].querySelector(`input[name=${key}]`);
            const select = formulario[1].querySelector(`select[name=${key}]`);

            if (input != null) {
                if (input.type === 'radio') {
                    if (key === 'vive_con_alumno') alternarDireccionMdr(!val);

                    const checkbox = formulario[1].querySelector(`input[name=${key}][value=${val}]`);
                    checkbox.checked = true;
                } else {
                    input.value = val;
                }
            }
            if (select != null) {
                if (select.name == 'region') region[1].dispatchEvent(new Event('change'));
                if (select.name == 'comuna') setTimeout(() => select.value = val, 500)
                select.value = val;
            }
        });
    } catch (err) {
        showMessage('Ha ocurrido un error interno.', 5000);
        console.log(err);
    }
});
region[0].addEventListener('change', async (ev) => {
    comuna[0].innerHTML = '<option value="" selected>Elija una opcion</option>'

    const request = await fetch('/static/environment/comunas.json');
    const response = await request.json();

    const comunas = response[ev.target.value];
    for (let data of comunas) {
        comuna[0].innerHTML += `<option value="${data.id}">${data.name}</option>`;
    }
});
region[1].addEventListener('change', async (ev) => {
    comuna[1].innerHTML = '<option value="" selected>Elija una opcion</option>'

    const request = await fetch('/static/environment/comunas.json');
    const response = await request.json();

    const comunas = response[ev.target.value];
    for (let data of comunas) {
        comuna[1].innerHTML += `<option value="${data.id}">${data.name}</option>`;
    }
});

formulario[1].addEventListener('submit', async (ev) => {
    ev.preventDefault();

    const query_principal = formulario[0].querySelectorAll('input, select');
    const query_suplente = formulario[1].querySelectorAll('input, select');
    let body = {
        'principal': {},
        'suplente': {}
    }

    for (const data_principal of query_principal) {
        if (data_principal.type == 'radio') {
            if (data_principal.checked) {
                body.principal[data_principal.name] = data_principal.value;
            }
        } else {
            body.principal[data_principal.name] = data_principal.value;
        }
    }
    for (const data_suplente of query_suplente) {
        if (data_suplente.type == 'radio') {
            if (data_suplente.checked) {
                body.suplente[data_suplente.name] = data_suplente.value;
            }
        } else {
            body.suplente[data_suplente.name] = data_suplente.value;
        }
    }
    body = format(body);
    showMessage('Validan informacion, por favor espere...');
    
    try {
        const token = getCookie('csrftoken');

        const request = await fetch(`/createApoderado/${matricula.id}`, { headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token }, method: 'POST', body: body });
        const response = await request.json();
        
        if (response.ok) {
            showMessage('Gracias por matricular a su hijo.');
            setTimeout(() => {
                location.href = `/matricula-ok/${matricula.id}`;
            }, 5000);
        }
    } catch (err) {
        showMessage(err);
    }
})

function format(data) {
    data.principal['rut'] = data.principal['rut'].replace(/[^0-9kK]/g, '');
    data.suplente['rut'] = data.suplente['rut'].replace(/[^0-9kK]/g, '');

    data.principal['p_nombre'] = data.principal['nombres'].split(' ')[0];
    data.principal['s_nombre'] = data.principal['nombres'].split(' ').slice(1).join(' ');

    data.suplente['p_nombre'] = data.suplente['nombres'].split(' ')[0];
    data.suplente['s_nombre'] = data.suplente['nombres'].split(' ').slice(1).join(' ');

    data.suplente['vive_con_alumno'] = data.suplente['vive_con_alumno'] == 'true' ? true : false;
    data.principal['vive_con_alumno'] = data.principal['vive_con_alumno'] == 'true' ? true : false;

    return JSON.stringify(data);
}
function alternarDireccionPdr(bool) {
    const direccion = formulario[0].querySelector('.hidden');
    const option = bool ? 'block' : 'none';

    direccion.style.display = option;
}
function alternarDireccionMdr(bool) {
    const direccion = formulario[1].querySelector('.hidden');
    const option = bool ? 'block' : 'none';

    direccion.style.display = option;
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