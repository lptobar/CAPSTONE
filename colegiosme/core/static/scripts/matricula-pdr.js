const formulario = document.querySelectorAll('#matricula');
const rut = document.querySelectorAll('input[name=rut]');
const region = document.querySelectorAll('select[name=region]');
const comuna = document.querySelectorAll('select[name=comuna]');
const toastcontroller = document.querySelector('.toast-message');
const matricula = document.currentScript.dataset;

window.onload = async () => {
    try {
        const request = await fetch(`/getFatherInfo/${matricula.id}`);
        const response = await request.json();

        if (!response['ok']) {
            return;
        }

        if (Object.keys(response['data']['padre']).length > 0) {
            Object.entries(response['data']['padre']).map(entry => {
                const [key , val] = entry;
                const input = formulario[0].querySelector(`input[name=${key}]`);
                const select = formulario[0].querySelector(`select[name=${key}]`)
    
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
                    if (select.name === 'region') region[0].dispatchEvent(new Event('change'))
                    if (select.name === 'comuna') setTimeout(() => select.value = val, 500)
                    select.value = val;
                }
            });   
        }
        if (Object.keys(response['data']['madre']).length > 0) {
            Object.entries(response['data']['madre']).map(entry => {
                const [key , val] = entry;
                const input = formulario[1].querySelector(`input[name=${key}]`);
                const select = formulario[1].querySelector(`select[name=${key}]`)
    
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
                    if (select.name === 'region') region[1].dispatchEvent(new Event('change'))
                    if (select.name === 'comuna') setTimeout(() => select.value = val, 500)
                    select.value = val;
                }
            });   
        }
        
        setTimeout(() => {
            rut[0].dispatchEvent(new Event('blur'));
            rut[1].dispatchEvent(new Event('blur'));
        }, 500);
    } catch (err) {
        console.log(err);
    }
}

rut[0].addEventListener('blur', async (ev) => {
    if (ev.target.value.length < 2 || ev.target.value === '') return;

    // FORMAT RUN
    let run = ev.target.value.replace(/[^0-9kK]/g, '')
    ev.target.value = run.replace(/(\w)(\w)$/, '$1-$2');

    // GET INFO ABOUT PERSON
    const request = await fetch(`/getPerson/${run}`);
    const response = await request.json();

    if (!response['ok']) {
        return;
    }
    
    // FILL DATA IN FORM
    Object.entries(response['data']).map(entry => {
        const [key, val] = entry;

        const input = formulario[0].querySelector(`input[name=${key}]`);
        const select = formulario[0].querySelector(`select[name=${key}]`);

        if (input !== null) {
            if (input.type === 'radio') {
                if (key === 'vive_con_alumno') alternarDireccionPdr(!val);

                const checkbox = formulario[0].querySelector(`input[name=${key}][value=${val}]`);
                checkbox.checked = true;
            } else {
                input.value = val;
            }
        }
        if (select !== null) {
            if (select.name === 'region') region[0].dispatchEvent(new Event('change'))
            select.value = val;
        }
    });
});
rut[1].addEventListener('blur', async (ev) => {
    if (ev.target.value.length < 2 || ev.target.value === '') return;

    // FORMAT RUN
    let run = ev.target.value.replace(/[^0-9kK]/g, '')
    ev.target.value = run.replace(/(\w)(\w)$/, '$1-$2');

    // GET INFO ABOUT PERSON
    const request = await fetch(`/getPerson/${run}`);
    const response = await request.json();

    if (!response['ok']) {
        return;
    }
    
    // FILL DATA IN FORM
    Object.entries(response['data']).map(entry => {
        const [key, val] = entry;

        const input = formulario[1].querySelector(`input[name=${key}]`);
        const select = formulario[1].querySelector(`select[name=${key}]`);

        if (input !== null) {
            if (input.type === 'radio') {
                if (key === 'vive_con_alumno') alternarDireccionPdr(!val);

                const checkbox = formulario[0].querySelector(`input[name=${key}][value=${val}]`);
                checkbox.checked = true;
            } else {
                input.value = val;
            }
        }
        if (select !== null) {
            if (select.name === 'region') region[1].dispatchEvent(new Event('change'))
            select.value = val;
        }
    });
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

    const query_padre = formulario[0].querySelectorAll('input, select');
    const query_madre = formulario[1].querySelectorAll('input, select');
    let body = {
        'padre': {},
        'madre': {}
    };

    for (const data_padre of query_padre) {
        if (data_padre.type == 'radio') {
            if (data_padre.checked) {
                body.padre[data_padre.name] = data_padre.value;
            }
        } else {
            body.padre[data_padre.name] = data_padre.value;
        }
    }
    for (const data_madre of query_madre) {
        if (data_madre.type == 'radio') {
            if (data_madre.checked) {
                body.madre[data_madre.name] = data_madre.value;
            }
        } else {
            body.madre[data_madre.name] = data_madre.value;
        }
        
    }
    body = format(body)
    showMessage('Validando informacion...');
    
    try {
        const token = getCookie('csrftoken');

        const request = await fetch(`/createFather/${matricula.id}`, { headers: { 'Content-Type':  'application/json', 'X-CSRFToken': token }, method: 'POST', body: body });
        const response = await request.json();

        if (response.ok) {
            showMessage('Informacion correcta, redirigiendo...');
            setTimeout(() => {
                location.href = `/matricula-apd/${matricula.id}`;
            }, 5000);
        }
    } catch (err) {
        console.log(err);
        showMessage('Hubo un error interno...');
    }
});

function format(data) {
    data.padre['rut'] = data.padre['rut'].replace(/[^0-9kK]/g, '');
    data.madre['rut'] = data.madre['rut'].replace(/[^0-9kK]/g, '');

    data.padre['p_nombre'] = data.padre['nombres'].split(' ')[0];
    data.padre['s_nombre'] = data.padre['nombres'].split(' ').slice(1).join(' ');

    data.madre['p_nombre'] = data.madre['nombres'].split(' ')[0];
    data.madre['s_nombre'] = data.madre['nombres'].split(' ').slice(1).join(' ');

    data.madre['vive_con_alumno'] = data.madre['vive_con_alumno'] == 'true' ? true : false;
    data.padre['vive_con_alumno'] = data.padre['vive_con_alumno'] == 'true' ? true : false;

    return JSON.stringify(data);
}
function alternarDireccionPdr(mostrar) {
    const direccionPdr = formulario[0].querySelector('.hidden');
    const option = mostrar ? 'block' : 'none';

    direccionPdr.style.display = option;
}
function alternarDireccionMdr(mostrar) {
    const direccionMdr = formulario[1].querySelector('.hidden');
    const option = mostrar ? 'block' : 'none';

    direccionMdr.style.display = option;
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