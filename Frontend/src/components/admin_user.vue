<script setup>
    import axios from 'axios'
    import { onMounted, ref } from 'vue'
    const users = ref([])
    const message = ref('')
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('role') || 'admin'
    onMounted(async () => {
        try {
            const pat = await axios.get('http://localhost:5000/admin/users', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            users.value = pat.data.users
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    })
</script>

<template>
    <div class="container mt-4">
        <nav class="nav flex-column flex-lg-row mb-4 bg-light p-3">
            <router-link class="nav-link" to="/admin/home">Home</router-link>
            <router-link class="nav-link active" to="/admin/users">Users</router-link>
            <router-link class="nav-link" to="/admin/search">Search</router-link>
            <router-link class="nav-link" to="/admin/summary">Summary</router-link>
            <router-link class="nav-link" to="/logout">Logout</router-link>
            <router-link class="nav-link" :to="`/${role}/edit_profile`">Edit Profile</router-link>
        </nav>
        <h2 class="mb-3">Registered Users</h2>
        <div v-if="message" class="alert alert-danger" role="alert">
            {{ message }}
        </div>
        <div v-if="users.length">
            <div class="table-responsive">
                <table class="table table-striped table-bordered">
                    <thead class="table-dark">
                        <tr>
                            <th scope="col">ID</th>
                            <th scope="col">Full Name</th>
                            <th scope="col">Email</th>
                            <th scope="col">Address</th>
                            <th scope="col">Pincode</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in users" :key="user.id">
                            <td>{{ user.id }}</td>
                            <td>{{ user.full_name }}</td>
                            <td>{{ user.email_id }}</td>
                            <td>{{ user.address }}</td>
                            <td>{{ user.pincode }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div v-else class="alert alert-info" role="alert">
            No users registered.
        </div>
    </div>
</template>

<style scoped>
.nav-link {
    color: #007bff;
    padding: 0.5rem 1rem;
}
.nav-link:hover {
    color: #0056b3;
    background-color: #f8f9fa;
}
.nav-link.active {
    color: #ffffff;
    background-color: #007bff;
    border-radius: 0.25rem;
}
.table th, .table td {
    vertical-align: middle;
}
</style>