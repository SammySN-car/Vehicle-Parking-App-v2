<script setup>
    import { onMounted, ref } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import axios from 'axios'

    const message = ref('')
    const route = useRoute()
    const router = useRouter()
    const lot_id = parseInt(route.params.lot_id)
    const token = localStorage.getItem('token')

    onMounted(async () => {
        try {
            await axios.delete(`http://localhost:5000/admin/delete_lot/${lot_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            message.value = "Lot has been deleted successfully"
            setTimeout(() => {
                router.push('/admin/home')
            }, 3000)
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    })
</script>

<template>
    <div class="container mt-5 text-center">
        <div v-if="message" class="alert" :class="message.includes('success') ? 'alert-success' : 'alert-danger'" role="alert">
            {{ message }}
        </div>
    </div>
</template>