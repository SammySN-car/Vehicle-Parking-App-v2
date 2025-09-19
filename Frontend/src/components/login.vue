<script setup>
    import axios from 'axios'
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    const form = ref({ email_id: '', password: '' })
    const message = ref('')
    const router = useRouter()

    const login = async () => {
        try {
            const pat = await axios.post('http://localhost:5000/', form.value)
            const token = pat.data.token
            const role = pat.data.role
            const id = pat.data.id
            const file_name='none'

            localStorage.setItem('token', token)
            localStorage.setItem('role', role)
            localStorage.setItem('id', id)
            localStorage.setItem('file_name', file_name)

            message.value = 'Login successful'

            if (role === 'admin') {
                router.push('/admin/home')
            } else {
                router.push('/user/home')
            }
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    }
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h3 class="text-center mb-4">Login</h3>
                <div v-if="message" class="alert" :class="message === 'Login successful' ? 'alert-success' : 'alert-danger'" role="alert">
                    {{ message }}
                </div>
                <form @submit.prevent="login">
                    <div class="mb-3">
                        <label for="email_id" class="form-label">Email</label>
                        <input type="email" class="form-control" id="email_id" name="email_id" v-model="form.email_id" required placeholder="Enter your email">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" v-model="form.password" required placeholder="Enter your password">
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
                <div class="text-center mt-3">
                    <p>Don't have an account? <router-link to="/register" class="link-primary">Register here</router-link></p>
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