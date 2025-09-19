<script setup>
    import axios from 'axios'
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    const form = ref({
        full_name: '',
        email_id: '',
        password: '',
        pincode: '',
        address: ''
    })
    const message = ref('')
    const router = useRouter()

    const register = async () => {
        try {
            const pat = await axios.post('http://localhost:5000/register', form.value)
            message.value = pat.data.message
            router.push('/')
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    }
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h3 class="text-center mb-4">Register</h3>
                <div v-if="message" class="alert" :class="message.includes('success') ? 'alert-success' : 'alert-danger'" role="alert">
                    {{ message }}
                </div>
                <form @submit.prevent="register">
                    <div class="mb-3">
                        <label for="full_name" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="full_name" name="full_name" v-model="form.full_name" required placeholder="Enter your full name">
                    </div>
                    <div class="mb-3">
                        <label for="email_id" class="form-label">Email</label>
                        <input type="email" class="form-control" id="email_id" name="email_id" v-model="form.email_id" required placeholder="Enter your email">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" v-model="form.password" required placeholder="Enter your password">
                    </div>
                    <div class="mb-3">
                        <label for="address" class="form-label">Address</label>
                        <input type="text" class="form-control" id="address" name="address" v-model="form.address" required placeholder="Enter your address">
                    </div>
                    <div class="mb-3">
                        <label for="pincode" class="form-label">Pincode</label>
                        <input type="text" class="form-control" id="pincode" name="pincode" v-model="form.pincode" required placeholder="Enter your pincode">
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Register</button>
                </form>
                <div class="text-center mt-3">
                    <p>Already have an account? <router-link to="/" class="link-primary">Login here</router-link></p>
                </div>
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