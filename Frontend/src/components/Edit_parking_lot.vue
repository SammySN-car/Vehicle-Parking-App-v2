<script setup>
    import { onMounted, ref } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import axios from 'axios'

    const form = ref({
        prime_location_name: '',
        address: '',
        pincode: '',
        price: '',
        maximum_number_of_spots: ''
    })
    const router = useRouter()
    const route = useRoute()
    const message = ref('')
    const lot_id = parseInt(route.params.lot_id)
    const token = localStorage.getItem('token')

    onMounted(async () => {
        try {
            const pat = await axios.get(`http://localhost:5000/admin/edit_lot/${lot_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            form.value.prime_location_name = pat.data.lot_details.prime_location_name
            form.value.address = pat.data.lot_details.address
            form.value.pincode = pat.data.lot_details.pincode
            form.value.price = pat.data.lot_details.price
            form.value.maximum_number_of_spots = pat.data.lot_details.maximum_number_of_spots
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    })
    const Edit_lot = async () => {
        try {
            await axios.put(`http://localhost:5000/admin/edit_lot/${lot_id}`, form.value, {
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
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h2 class="text-center mb-4">Edit Parking Lot</h2>
                <div v-if="message" class="alert alert-danger" role="alert">
                    {{ message }}
                </div>
                <form @submit.prevent="Edit_lot">
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
                    <button type="submit" class="btn btn-primary w-100">Update</button>
                </form>
                <button type="button" class="btn btn-secondary w-100 mt-3" @click="router.push('/admin/home')">Back</button>
            </div>
        </div>
    </div>
</template>