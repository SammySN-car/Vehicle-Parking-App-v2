<script setup>
    import { useRouter } from 'vue-router'

    const router = useRouter()
    localStorage.removeItem('token')
    router.push('/')
</script>

<template>
    <div class="container mt-5 text-center">
        <div class="alert alert-info" role="alert">
            Logging out... Redirecting to login page
        </div>
    </div>
</template>