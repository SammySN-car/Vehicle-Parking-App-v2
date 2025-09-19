<script setup>
    import axios from 'axios'
    import { ref } from 'vue'

    const role = localStorage.getItem('role') || 'admin'
    const token = localStorage.getItem('token')
    const form = ref({
        search_by: '',
        search_term: ''
    })
    const results = ref([])
    const message = ref('')

    const Search_is = async () => {
        try {
            const pat = await axios.post('http://localhost:5000/admin/search', form.value, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            results.value = pat.data.results
        } catch (err) {
            message.value = err.response?.data?.message || 'Error occurred'
        }
    }
</script>

<template>
    <div class="container mt-4">
        <nav class="nav flex-column flex-lg-row mb-4 bg-light p-3">
            <router-link class="nav-link" to="/admin/home">Home</router-link>
            <router-link class="nav-link" to="/admin/users">Users</router-link>
            <router-link class="nav-link active" to="/admin/search">Search</router-link>
            <router-link class="nav-link" to="/admin/summary">Summary</router-link>
            <router-link class="nav-link" to="/logout">Logout</router-link>
            <router-link class="nav-link" :to="`/${role}/edit_profile`">Edit Profile</router-link>
        </nav>
        <div v-if="message" class="alert alert-danger" role="alert">
            {{ message }}
        </div>
        <form @submit.prevent="Search_is" class="mb-4">
            <div class="row">
                <div class="col-md-4">
                    <label for="search_by" class="form-label">Search by</label>
                    <select name="search_by" class="form-select" id="search_by" v-model="form.search_by" required>
                        <option value="" disabled>Select an option</option>
                        <option value="user_id">User ID</option>
                        <option value="prime_location_name">Parking Location</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label for="search_term" class="form-label">Search Term</label>
                    <input type="text" class="form-control" id="search_term" name="search_term" v-model="form.search_term" required placeholder="Enter search term">
                </div>
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary w-100">Search</button>
                </div>
            </div>
        </form>
        <hr>
        <div v-if="results.length">
            <div v-if="form.search_by === 'user_id'">
                <h3 class="mb-3">User Details</h3>
                <div class="table-responsive">
                    <table class="table table-striped table-bordered">
                        <thead class="table-dark">
                            <tr>
                                <th scope="col">ID</th>
                                <th scope="col">Full Name</th>
                                <th scope="col">Email</th>
                                <th scope="col">Address</th>
                                <th scope="col">Pincode</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in results" :key="user.id">
                                <td>{{ user.id }}</td>
                                <td>{{ user.full_name }}</td>
                                <td>{{ user.email_id }}</td>
                                <td>{{ user.address }}</td>
                                <td>{{ user.pincode }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div v-else-if="form.search_by === 'prime_location_name'">
                <h3 class="mb-3">Parking Lots Found</h3>
                <div class="table-responsive">
                    <table class="table table-striped table-bordered">
                        <thead class="table-dark">
                            <tr>
                                <th scope="col">ID</th>
                                <th scope="col">Location</th>
                                <th scope="col">Price (₹)</th>
                                <th scope="col">Address</th>
                                <th scope="col">Pincode</th>
                                <th scope="col">Occupied</th>
                                <th scope="col">Available</th>
                                <th scope="col">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in results" :key="item.id">
                                <td>{{ item.id }}</td>
                                <td>{{ item.prime_location_name }}</td>
                                <td>{{ item.price }}</td>
                                <td>{{ item.address }}</td>
                                <td>{{ item.pincode }}</td>
                                <td>{{ item.occupied }}</td>
                                <td>{{ item.available }}</td>
                                <td>
                                    <router-link :to="`/admin/edit_lot/${item.id}`" class="btn btn-outline-primary btn-sm">Edit</router-link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div v-else-if="form.search_by" class="alert alert-info" role="alert">
            No results found.
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