<script setup>
    import axios from 'axios'
    import { onMounted, ref } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    const route = useRoute()
    const router = useRouter()
    const lot_id = parseInt(route.params.lot_id)
    const token = localStorage.getItem('token')
    const user_id = ref(localStorage.getItem('id'))
    const message = ref('')
    const mesage = ref('')
    const spot = ref({
        'id': '',
        'lot_id': '',
        'vehicle_number': ''
    })

    onMounted(async () => {
        try {
            const pat = await axios.get(`http://localhost:5000/user/book/${lot_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            spot.value.id = pat.data.spot.id
            spot.value.lot_id = pat.data.spot.lot_id
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    })
    const UserBook = async () => {
        try {
            await axios.post(`http://localhost:5000/user/book/${lot_id}`, spot.value, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            mesage.value = 'Booking successful'
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
                <h2 class="text-center mb-4">Book Slot</h2>
                <div v-if="message" class="alert alert-danger" role="alert">
                    {{ message }}
                </div>
                <div v-if="mesage" class="alert alert-success" role="alert">
                    {{ mesage }}
                </div>
                <form @submit.prevent="UserBook">
                    <div class="mb-3">
                        <label for="user_id" class="form-label">User ID</label>
                        <input type="number" class="form-control" id="user_id" name="user_id" v-model.number="user_id" readonly required>
                    </div>
                    <div class="mb-3">
                        <label for="spot_id" class="form-label">Spot ID</label>
                        <input type="number" class="form-control" id="spot_id" name="spot_id" v-model.number="spot.id" readonly required>
                    </div>
                    <div class="mb-3">
                        <label for="lot_id" class="form-label">Lot ID</label>
                        <input type="number" class="form-control" id="lot_id" name="lot_id" v-model.number="spot.lot_id" readonly required>
                    </div>
                    <div class="mb-3">
                        <label for="vehicle_number" class="form-label">Vehicle Number</label>
                        <input type="text" class="form-control" id="vehicle_number" name="vehicle_number" v-model="spot.vehicle_number" required placeholder="Enter vehicle number">
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Book</button>
                </form>
                <button type="button" class="btn btn-secondary w-100 mt-3" @click="router.push('/user/home')">Back</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.link-primary {
    text-decoration: none;
}
.link-primary:hover {
    text-decoration: underline;
}
</style>