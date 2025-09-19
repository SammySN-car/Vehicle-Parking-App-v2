import Login from '@/components/login.vue'
import Register from '@/components/register.vue'
import admin_dashboard from '@/components/admin_dashboard.vue'
import Add_parking_lot from '@/components/Add_parking_lot.vue'
import Edit_parking_lot from '@/components/Edit_parking_lot.vue'
import admin_search from '@/components/admin_search.vue'
import Admin_spot from '@/components/Admin_spot.vue'
import admin_summary from '@/components/admin_summary.vue'
import admin_user from '@/components/admin_user.vue'
import delete_lot from '@/components/delete_lot.vue'
import edit_profile from '@/components/edit_profile.vue'
import user_book from '@/components/user_book.vue'
import user_dashboard from '@/components/user_dashboard.vue'
import user_release from '@/components/user_release.vue'
import user_summary from '@/components/user_summary.vue'
import UserExportcsv from '@/components/UserExportcsv.vue'
import logout from '@/components/logout.vue'

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/admin/home',
      name: 'admin_home',
      component: admin_dashboard
    },
    {
      path: '/admin/add_lot',
      name: 'admin_add_lot',
      component: Add_parking_lot
    },
    {
      path: '/admin/search',
      name: 'admin_search',
      component: admin_search
    },
    {
      path: '/admin/spot/:spot_id',
      name: 'admin_spot',
      component: Admin_spot
    },
    {
      path: '/admin/summary',
      name: 'admin_summary',
      component: admin_summary
    },
    {
      path: '/admin/users',
      name: 'admin_users',
      component: admin_user
    },
    {
      path: '/admin/delete_lot/:lot_id',
      name: 'admin_delete',
      component: delete_lot
    },
    {
      path: '/admin/edit_lot/:lot_id',
      name: 'admin_edit',
      component: Edit_parking_lot
    },
    {
      path: '/:role/edit_profile',
      name: 'edit_profile',
      component: edit_profile
    },
    {
      path: '/logout',
      name: 'logout',
      component: logout
    },
    {
      path: '/user/book/:lot_id',
      name: 'user_book',
      component: user_book
    },
    {
      path: '/user/home',
      name: 'user_home',
      component: user_dashboard
    },
    {
      path: '/user/release/:reservation_id',
      name: 'user_release',
      component: user_release
    },
    {
      path: '/user/summary',
      name: 'user_summary',
      component: user_summary
    },
    {
      path: '/user/export_csv',
      name: 'user_export',
      component: UserExportcsv
    }
  ],
})

export default router
