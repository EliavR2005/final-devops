const modal          = document.getElementById('passModal');
const form           = document.getElementById('passForm');
const adminPassInput = document.getElementById('adminPass');
let targetUsername   = null;
let currentAction    = null; // 'view' o 'edit'

// Al hacer click en cualquiera de los botones “Ver” o “Editar”
document.querySelectorAll('.openViewModalBtn, #openEditModalBtn').forEach(btn => {
  btn.addEventListener('click', () => {
    targetUsername = btn.dataset.username;
    // Referenciamos según el id o clase del botón
    currentAction = btn.classList.contains('openViewModalBtn') ? 'view' : 'edit';
    modal.showModal();
  });
});

// Cancelar modal
document.getElementById('cancelBtn').addEventListener('click', () => {
  modal.close();
});

// Cuando el admin envía contraseña
form.addEventListener('submit', async e => {
  e.preventDefault();
  modal.close();

  const pwd = adminPassInput.value;
  adminPassInput.value = '';

  // Llamamos a la ruta de descifrado
  const resp = await fetch(`/user/${targetUsername}/encrypted`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ admin_password: pwd })
  });
  const data = await resp.json();
  if (!resp.ok) {
    alert(data.error);
    return;
  }

  if (currentAction === 'view') {
    // Reemplaza los <li> con los datos descifrados
    const items = document.querySelectorAll('ul > li');
    items[1].textContent = `Email: ${data.email}`;
    items[2].textContent = `Dirección: ${data.address}`;
    items[3].textContent = `Teléfono: ${data.phone}`;
    items[4].textContent = `RFC: ${data.rfc}`;
  }
  else if (currentAction === 'edit') {
    // Muestra el formulario de edición
    document.getElementById('editFormContainer').style.display = 'block';
    // Opcional: el prefilling ya lo tienes con value="{{ data… }}"
  }
});