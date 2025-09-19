<script setup>
    import axios from 'axios'
    import { onMounted, ref } from 'vue'
    import { useRoute, useRouter } from 'vue-router'

    const token = localStorage.getItem('token')
    const spots = ref({
        id: '',
        status: '',
        user_id: '',
        vehicle_number: '',
        parking_timestamp: '',
        parking_cost: ''
    })
    const message = ref('')
    const route = useRoute()
    const spot_id = parseInt(route.params.spot_id)
    const router = useRouter()
    onMounted(async () => {
        try {
            const pat = await axios.get(`http://localhost:5000/admin/spot/${spot_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            spots.value.id = pat.data.spots.id
            spots.value.status = pat.data.spots.status
            if (pat.data.spots.occupied) {
                spots.value.user_id = pat.data.spots.occupied.user_id
                spots.value.vehicle_number = pat.data.spots.occupied.vehicle_number
                spots.value.parking_timestamp = pat.data.spots.occupied.parking_timestamp
                spots.value.parking_cost = pat.data.spots.occupied.parking_cost
            }
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    })
    const Delete_spot = async () => {
        try {
            await axios.delete(`http://localhost:5000/admin/spot/${spot_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            router.push('/admin/home')
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    }
</script>

<template>
    <div class="container mt-4">
        <h2 class="mb-3">Parking Spot Details</h2>
        <div v-if="message" class="alert alert-danger" role="alert">
            {{ message }}
        </div>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Spot ID: {{ spots.id }}</h5>
                <p class="card-text">Status: {{ spots.status }}</p>
                <div v-if="spots.status === 'O'">
                    <h3 class="card-subtitle mb-2">Occupied Parking Spot Details</h3>
                    <p class="card-text">Customer ID: {{ spots.user_id }}</p>
                    <p class="card-text">Vehicle Number: {{ spots.vehicle_number }}</p>
                    <p class="card-text">Date/Time of Parking: {{ spots.parking_timestamp }}</p>
                    <p class="card-text">Estimated Parking Cost: {{ spots.parking_cost }}</p>
                </div>
                <div v-else-if="spots.status === 'A'">
                    <button class="btn btn-danger" @click="Delete_spot">Delete</button>
                </div>
                <div v-else class="alert alert-warning" role="alert">
                    Cannot delete. Spot is occupied.
                </div>
                <button class="btn btn-secondary mt-3" @click="router.push('/admin/home')">Back</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.card {
    border-radius: 0.5rem;
}
</style>