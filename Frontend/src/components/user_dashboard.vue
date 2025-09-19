<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue'
    import { useRouter } from 'vue-router'
    import axios from 'axios'

    const search_term = ref('')
    const router = useRouter()
    const booked = ref([])
    const released = ref([])
    const details= ref([])
    const lots = ref([])
    const message = ref('')
    const userid= localStorage.getItem('id')
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('role') || 'user'
    const downl = ref('')
    const downR = ref(false)
    let starpoll = null

    const stpoll = () => {
        starpoll = setInterval(checkdownl, 3000)
    }
    onBeforeUnmount(() => {
        if (starpoll){
            clearInterval(starpoll)
            starpoll = null
    }})
    const cleardownl = () => {
        localStorage.removeItem('file_name')
        downR.value = false
        URL.revokeObjectURL(downl.value)
    }
    const checkdownl = async () => {
        const file_name = localStorage.getItem('file_name')
        if (!file_name) return

        try {
            const pat = await axios.get(`http://localhost:5000/user/export_csv/${file_name}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                },
                responseType: 'blob'
            })
            if (pat.status === 200) {
                downl.value = URL.createObjectURL(pat.data)
                downR.value = true
                if (starpoll) {
                    clearInterval(starpoll)
                    starpoll = null
                }
            }
        } catch {}
    }
    onMounted(async () => {
        try {
            const pat = await axios.get('http://localhost:5000/user/home', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            booked.value = pat.data.booked
            released.value = pat.data.released
            details.value=pat.data.details
            const file_name = localStorage.getItem('file_name')
            if (file_name!=='none') {
                stpoll()
            }
            
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    })
    const Search = async () => {
        try {
            const cat = await axios.post('http://localhost:5000/user/home', { search_term: search_term.value }, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            lots.value = cat.data.lots
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    }
</script>

<template>
    <div class="container mt-4">
        <nav class="nav flex-column flex-lg-row mb-4 bg-light p-3">
            <router-link class="nav-link active" to="/user/home">Home</router-link>
            <router-link class="nav-link" to="/user/summary">Summary</router-link>
            <router-link class="nav-link" to="/logout">Logout</router-link>
            <router-link class="nav-link" :to="`/${role}/edit_profile`">Edit Profile</router-link>
        </nav>
        <div v-if="message" class="alert alert-danger" role="alert">
            {{ message }}
        </div>
        <h1 class="mb-3">Recent Parking History</h1>
        <div class="table-responsive">
            <table class="table table-striped table-bordered">
                <thead class="table-dark">
                    <tr>
                        <th scope="col">Reservation ID</th>
                        <th scope="col">Location</th>
                        <th scope="col">Vehicle No</th>
                        <th scope="col">Timestamp</th>
                        <th scope="col">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in booked" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.prime_location_name }}</td>
                        <td>{{ user.vehicle_number }}</td>
                        <td>None</td>
                        <td>
                            <button type="button" class="btn btn-primary btn-sm" @click="router.push(`/user/release/${user.id}`)">Release</button>
                        </td>
                    </tr>
                    <tr v-for="user in released" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.prime_location_name }}</td>
                        <td>{{ user.vehicle_number }}</td>
                        <td>{{ user.leaving_timestamp }}</td>
                        <td>Already Released</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <hr>
        <form @submit.prevent="Search" class="mb-4">
            <div class="row">
                <div class="col-md-8">
                    <label for="search_term" class="form-label">Search Parking</label>
                    <input type="text" class="form-control" id="search_term" name="search_term" v-model="search_term" placeholder="Search by location or pincode" required>
                </div>
                <div class="col-md-4 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary w-100">Search</button>
                </div>
            </div>
        </form>
        <div class="table-responsive">
            <table class="table table-striped table-bordered">
                <thead class="table-dark">
                    <tr>
                        <th scope="col">Lot ID</th>
                        <th scope="col">Address</th>
                        <th scope="col">Available</th>
                        <th scope="col">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in lots" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.prime_location_name }}</td>
                        <td>{{ user.available }}</td>
                        <td>
                            <button type="button" class="btn btn-primary btn-sm" @click="router.push(`/user/book/${user.id}`)">Book</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <hr>
        <div class="table-responsive">
            <table class="table table-striped table-bordered">
                <thead class="table-dark">
                    <tr>
                        <th scope="col">Lot ID</th>
                        <th scope="col">Address</th>
                        <th scope="col">Available</th>
                        <th scope="col">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in details" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.prime_location_name }}</td>
                        <td>{{ user.available }}</td>
                        <td>
                            <button type="button" class="btn btn-primary btn-sm" @click="router.push(`/user/book/${user.id}`)">Book</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <button type="button" class="btn btn-primary mt-3" @click="router.push('/user/export_csv')">Export Your Details</button>
        <div v-if="downR" class="alert alert-success mt-3" role="alert">
            Your CSV file is ready!
            <a :href="downl" target="_blank" class="btn btn-success btn-sm mt-2" download="your_csv" >Download CSV</a>
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
.table th, .table td {
    vertical-align: middle;
}
</style>