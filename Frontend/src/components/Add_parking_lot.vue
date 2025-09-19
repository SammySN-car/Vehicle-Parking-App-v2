<script setup>
    import { useRouter } from 'vue-router'
    import axios from 'axios'
    import { ref } from 'vue'

    const form = ref({
        prime_location_name: '',
        address: '',
        pincode: '',
        price: '',
        maximum_number_of_spots: ''
    })
    const token = localStorage.getItem('token')
    const message = ref('')
    const router = useRouter()

    const Add_lot = async () => {
        try {
            const pat = await axios.post('http://localhost:5000/admin/add_lot', form.value, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            message.value = pat.data.message
            router.push('/admin/home')
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    }
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h3 class="text-center mb-4">Add Parking Lot</h3>
                <div v-if="message" class="alert" :class="message.includes('success') ? 'alert-success' : 'alert-danger'" role="alert">
                    {{ message }}
                </div>
                <form @submit.prevent="Add_lot">
                    <div class="mb-3">
                        <label for="prime_location_name" class="form-label">Location Name</label>
                        <input type="text" class="form-control" id="prime_location_name" name="prime_location_name" v-model="form.prime_location_name" required placeholder="Enter location name">
                    </div>
                    <div class="mb-3">
                        <label for="address" class="form-label">Address</label>
                        <input type="text" class="form-control" id="address" name="address" v-model="form.address" required placeholder="Enter address">
                    </div>
                    <div class="mb-3">
                        <label for="pincode" class="form-label">Pincode</label>
                        <input type="number" class="form-control" id="pincode" name="pincode" v-model.number="form.pincode" required placeholder="Enter pincode">
                    </div>
                    <div class="mb-3">
                        <label for="price" class="form-label">Price</label>
                        <input type="number" class="form-control" id="price" name="price" v-model.number="form.price" required placeholder="Enter price">
                    </div>
                    <div class="mb-3">
                        <label for="maximum_number_of_spots" class="form-label">Maximum Spots</label>
                        <input type="number" class="form-control" id="maximum_number_of_spots" name="maximum_number_of_spots" v-model.number="form.maximum_number_of_spots" required placeholder="Enter maximum spots">
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Add</button>
                </form>
                <button type="button" class="btn btn-secondary w-100 mt-3" @click="router.push('/admin/home')">Back</button>
            </div>
        </div>
    </div>
</template>