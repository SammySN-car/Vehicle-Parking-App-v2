<script setup>
    import { BarController, BarElement, CategoryScale, Chart, LinearScale, PieController, ArcElement } from 'chart.js'
    import { onMounted, ref } from 'vue'
    import axios from 'axios'

    Chart.register(BarController, BarElement, CategoryScale, LinearScale, PieController, ArcElement)
    const chartCanvas = ref(null)
    const chartCanvasnew = ref(null)
    const token = localStorage.getItem('token')
    const message = ref('')
    const role = localStorage.getItem('role')
    const chart_is = ref(true)
    const newchart = ref(null)
    const newpie = ref(null)

    onMounted(async () => {
        try {
            const pat = await axios.get('http://localhost:5000/admin/summary', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            const lot = pat.data.summary.loty
            const available = pat.data.summary.availablety
            const occupied = pat.data.summary.occupiedity
            const revenue = pat.data.summary.revenuety
            if (!lot || lot.length === 0) {
                message.value = 'No data available'
                chart_is.value = false
                return
            }
            if (newchart.value) {
                newchart.value.destroy()
            }
            if (newpie.value) {
                newpie.value.destroy()
            }
            const labels = lot.map(d => `Lot ${d}`)

            if (available.length > 0 || occupied.length > 0) {
                newchart.value = new Chart(chartCanvas.value, {
                    type: 'bar',
                    data: {
                        labels,
                        datasets: [
                            {
                                label: 'Available',
                                data: available,
                                backgroundColor: 'rgba(75,192,192,0.6)'
                            },
                            {
                                label: 'Occupied',
                                data: occupied,
                                backgroundColor: 'rgba(255,99,132,0.6)'
                            }
                        ]
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
            }
            if (revenue.length > 0) {
                newpie.value = new Chart(chartCanvasnew.value, {
                    type: 'pie',
                    data: {
                        labels,
                        datasets: [{
                            label: 'Revenue distribution',
                            data: revenue,
                            backgroundColor: 'rgba(75,192,192,0.6)'
                        }]
                    },
                    options: {
                        responsive: true,
                    }
                })
            }
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
            <router-link class="nav-link" to="/admin/home">Home</router-link>
            <router-link class="nav-link" to="/admin/users">Users</router-link>
            <router-link class="nav-link" to="/admin/search">Search</router-link>
            <router-link class="nav-link active" to="/admin/summary">Summary</router-link>
            <router-link class="nav-link" to="/logout">Logout</router-link>
            <router-link class="nav-link" :to="`/${role}/edit_profile`">Edit Profile</router-link>
        </nav>
        <div v-if="message" class="alert alert-danger" role="alert">
            {{ message }}
        </div>
        <div v-if="chart_is" class="row">
            <div class="col-md-6 mb-4">
                <h3 class="mb-3">Spot Availability</h3>
                <canvas ref="chartCanvas"></canvas>
            </div>
            <div class="col-md-6 mb-4">
                <h3 class="mb-3">Revenue Distribution</h3>
                <canvas ref="chartCanvasnew"></canvas>
            </div>
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