// Base API URL
const API_URL = 'http://10.0.2.11:5000'; // Replace with your Flask backend IP/domain

// Add User Form Submission
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('addUserForm');
    if(form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const role = document.getElementById('role').value;
            const email = document.getElementById('email').value;

            const res = await fetch(`${API_URL}/add_user`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password, role, email})
            });

            if(res.ok) {
                alert('User added successfully!');
                loadUsers();
                form.reset();
            } else {
                alert('Error adding user!');
            }
        });
    }

    loadUsers();
});

// Load Users from Backend
async function loadUsers() {
    const res = await fetch(`${API_URL}/list_users`);
    if(!res.ok) return;
    const users = await res.json();
    const tbody = document.getElementById('userTableBody');
    tbody.innerHTML = '';
    users.forEach(u => {
        tbody.innerHTML += `<tr>
            <td class="border px-4 py-2">${u.id}</td>
            <td class="border px-4 py-2">${u.username}</td>
            <td class="border px-4 py-2">${u.role}</td>
            <td class="border px-4 py-2">${u.email}</td>
        </tr>`;
    });
}
