<script setup>
    import { onMounted, ref } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import axios from 'axios'

    const form = ref({
        full_name: '',
        address: '',
        pincode: '',
        password: ''
    })
    const token = localStorage.getItem('token')
    const route = useRoute()
    const router = useRouter()
    const role = localStorage.getItem('role')
    const message = ref('')

    onMounted(async () => {
        try {
            const pat = await axios.get(`http://localhost:5000/${role}/edit_profile`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            form.value.full_name = pat.data.user_details.full_name
            form.value.address = pat.data.user_details.address
            form.value.pincode = pat.data.user_details.pincode
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    })

    const Edit_profile = async () => {
        try {
            await axios.put(`http://localhost:5000/${role}/edit_profile`, form.value, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            router.push(`/${role}/home`)
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    }
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h2 class="text-center mb-4">Edit Profile</h2>
                <div v-if="message" class="alert alert-danger" role="alert">
                    {{ message }}
                </div>
                <form @submit.prevent="Edit_profile">
                    <div class="mb-3">
                        <label for="full_name" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="full_name" name="full_name" v-model="form.full_name" required placeholder="Enter your full name">
                    </div>
                    <div class="mb-3">
                        <label for="address" class="form-label">Address</label>
                        <input type="text" class="form-control" id="address" name="address" v-model="form.address" required placeholder="Enter your address">
                    </div>
                    <div class="mb-3">
                        <label for="pincode" class="form-label">Pincode</label>
                        <input type="number" class="form-control" id="pincode" name="pincode" v-model.number="form.pincode" required placeholder="Enter your pincode">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" v-model="form.password" required placeholder="Enter your password">
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Update</button>
                </form>
                <button type="button" class="btn btn-secondary w-100 mt-3" @click="router.push(`/${role}/home`)">Back to Dashboard</button>
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