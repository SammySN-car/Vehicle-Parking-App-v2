<script setup>
    import axios from 'axios'
    import { onMounted, ref } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    const route = useRoute()
    const router = useRouter()
    const reservation_id = parseInt(route.params.reservation_id)
    const token = localStorage.getItem('token')
    const message = ref('')
    const reservation = ref({
        'leaving_timestamp': '',
        'parking_cost': ''
    })
    const reserve = ref({
        vehicle_number: '',
        parking_timestamp: '',
        spot_id: ''
    })

    onMounted(async () => {
        try {
            const pat = await axios.get(`http://localhost:5000/user/release/${reservation_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            reservation.value.leaving_timestamp = pat.data.leaving_timestamp
            reservation.value.parking_cost = pat.data.parking_cost
            reserve.value.parking_timestamp = pat.data.reservation.parking_timestamp
            reserve.value.vehicle_number = pat.data.reservation.vehicle_number
            reserve.value.spot_id = pat.data.reservation.spot_id
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    })
    const UserRelease = async () => {
        try {
            await axios.post(`http://localhost:5000/user/release/${reservation_id}`, reservation.value, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            message.value = 'Released successful'
            setTimeout(() => { router.push('/user/home') }, 3000)
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    }
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h2 class="text-center mb-4">Release Slot</h2>
                <div v-if="message" class="alert" :class="message.includes('success') ? 'alert-success' : 'alert-danger'" role="alert">
                    {{ message }}
                </div>
                <form @submit.prevent="UserRelease">
                    <div class="mb-3">
                        <label for="spot_id" class="form-label">Spot ID</label>
                        <input type="number" class="form-control" id="spot_id" name="spot_id" v-model="reserve.spot_id" readonly required>
                    </div>
                    <div class="mb-3">
                        <label for="vehicle_number" class="form-label">Vehicle Number</label>
                        <input type="text" class="form-control" id="vehicle_number" name="vehicle_number" v-model="reserve.vehicle_number" readonly required>
                    </div>
                    <div class="mb-3">
                        <label for="parking_timestamp" class="form-label">Parking Timestamp</label>
                        <input type="text" class="form-control" id="parking_timestamp" name="parking_timestamp" v-model="reserve.parking_timestamp" readonly required>
                    </div>
                    <div class="mb-3">
                        <label for="leaving_timestamp" class="form-label">Leaving Timestamp</label>
                        <input type="text" class="form-control" id="leaving_timestamp" name="leaving_timestamp" v-model="reservation.leaving_timestamp" readonly required>
                    </div>
                    <div class="mb-3">
                        <label for="parking_cost" class="form-label">Parking Cost</label>
                        <input type="text" class="form-control" id="parking_cost" name="parking_cost" v-model="reservation.parking_cost" readonly required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Release</button>
                </form>
                <button type="button" class="btn btn-secondary w-100 mt-3" @click="router.push('/user/home')">Back</button>
            </div>
        </div>
    </div>
</template>