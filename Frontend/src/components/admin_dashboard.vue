<script setup>
    import { onMounted, ref } from 'vue'
    import axios from 'axios'
    import { useRouter } from 'vue-router'

    const router = useRouter()
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('role') || 'admin'
    const lots = ref([])
    const error = ref('')

    onMounted(async () => {
        if (!token) {
            router.push('/login')
            return
        }
        try {
            const pat = await axios.get('http://localhost:5000/admin/home', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            lots.value = pat.data.all_lot
        } catch (err) {
            error.value = err.response?.data?.message || 'Access denied'
        }
    })
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Welcome to Admin Dashboard</h2>
        <nav class="nav flex-column flex-lg-row mb-4 bg-light p-3">
            <router-link class="nav-link active" to="/admin/home">Home</router-link>
            <router-link class="nav-link" to="/admin/users">Users</router-link>
            <router-link class="nav-link" to="/admin/search">Search</router-link>
            <router-link class="nav-link" to="/admin/summary">Summary</router-link>
            <router-link class="nav-link" to="/logout">Logout</router-link>
            <router-link class="nav-link" :to="`/${role}/edit_profile`">Edit Profile</router-link>
        </nav>
        <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
        </div>
        <h3 class="mb-3">Parking Lots</h3>
        <div v-for="item in lots" :key="item.id" class="card mb-3">
            <div class="card-body">
                <h4 class="card-title">Parking {{ item.id }} - {{ item.prime_location_name }}</h4>
                <p class="card-text">Occupied: {{ item.Occupied }} / {{ item.maximum_number_of_spots }}</p>
                <router-link :to="`/admin/edit_lot/${item.id}`" class="btn btn-outline-primary btn-sm me-2">Edit</router-link>
                <router-link :to="`/admin/delete_lot/${item.id}`" class="btn btn-outline-danger btn-sm">Delete</router-link>
                <p class="mt-2">Spots:</p>
                <div class="d-flex flex-wrap gap-2">
                    <router-link v-for="spot in item.spots" :key="spot.id" :to="`/admin/spot/${spot.id}`" class="btn btn-outline-secondary btn-sm">
                        [{{ spot.status }}-{{ spot.id }}]
                    </router-link>
                </div>
            </div>
        </div>
        <hr>
        <button type="button" class="btn btn-primary" @click="router.push('/admin/add_lot')">Add Lot</button>
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
.card {
    border-radius: 0.5rem;
}
</style>