<script setup>
    import { BarController, BarElement, CategoryScale, Chart, LinearScale } from 'chart.js'
    import { onMounted, ref } from 'vue'
    import axios from 'axios'

    Chart.register(BarController, BarElement, CategoryScale, LinearScale)
    const chartCanvas = ref(null)
    const token = localStorage.getItem('token')
    const message = ref('')
    const role = localStorage.getItem('role')
    const chart_is = ref(true)
    const newchart = ref(null)
    onMounted(async () => {
        try {
            const pat = await axios.get('http://localhost:5000/user/summary', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            const summary = pat.data.summary
            if (!summary || summary.length === 0) {
                message.value = 'No data available'
                chart_is.value = false
                return
            }
            if (newchart.value) {
                newchart.value.destroy()
            }
            const labels = summary.map(d => `Lot ${d.lot_id}`)
            const values = summary.map(d => d.used)

            newchart.value = new Chart(chartCanvas.value, {
                type: 'bar',
                data: {
                    labels,
                    datasets: [{
                        label: 'Total Times Used',
                        data: values,
                        backgroundColor: 'rgba(75,192,192,0.6)'
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { precision: 0 }
                        }
                    }
                }
            })
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
            chart_is.value = false
            console.error(message.value)
        }
    })
</script>

<template>
    <div class="container mt-4">
        <nav class="nav flex-column flex-lg-row mb-4 bg-light p-3">
            <router-link class="nav-link" to="/user/home">Home</router-link>
            <router-link class="nav-link active" to="/user/summary">Summary</router-link>
            <router-link class="nav-link" to="/logout">Logout</router-link>
            <router-link class="nav-link" :to="`/${role}/edit_profile`">Edit Profile</router-link>
        </nav>
        <div v-if="message" class="alert alert-danger" role="alert">
            {{ message }}
        </div>
        <div v-if="chart_is">
            <h3 class="mb-3">Parking Usage Summary</h3>
            <canvas ref="chartCanvas"></canvas>
        </div>
        <div v-else class="alert alert-info" role="alert">
            {{ message }}
        </div>
    </div>
</template>

<style scoped>
.nav-link {
    color: #007bff;
    padding: 0.5rem 1rem;
}
.nav-link:hover {
    color: #0056b3;
    background-color: #f8f9fa;
}
.nav-link.active {
    color: #ffffff;
    background-color: #007bff;
    border-radius: 0.25rem;
}
</style>