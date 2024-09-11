

function alternarCargo(mostrar) {
    const cargoAdmin = document.querySelector('#cargoAdmin');
    const option = mostrar ? 'block' : 'none';

    cargoAdmin.style.display = option;
}