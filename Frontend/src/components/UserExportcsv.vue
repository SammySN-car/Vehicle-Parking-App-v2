<script setup>
    import axios from 'axios'
    import { onMounted } from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter()
    const token = localStorage.getItem('token')
    onMounted(async () => {
        try {
            const pat = await axios.get('http://localhost:5000/user/export_csv', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            const file_name = pat.data.file_name
            localStorage.setItem('file_name', file_name)
            alert("Your CSV file exportation has started")
            router.push('/user/home')
        } catch (err) {
            alert('Export failed')
            router.push('/user/home')
        }
    })
</script>

<template>
    <div class="container mt-5 text-center">
        <div class="alert alert-info" role="alert">
            Exporting CSV... Redirecting to dashboard
        </div>
    </div>
</template>