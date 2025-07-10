import { createRouter, createWebHistory } from 'vue-router'
import Companies from '../views/Companies.vue'
import Talents from '../views/Talents.vue'
import Communications from '../views/Communications.vue'
import Certificates from '../views/Certificates.vue'

const routes = [
  {
    path: '/',
    redirect: '/companies'
  },
  {
    path: '/companies',
    name: 'Companies',
    component: Companies
  },
  {
    path: '/talents',
    name: 'Talents',
    component: Talents
  },
  {
    path: '/communications',
    name: 'Communications',
    component: Communications
  },
  {
    path: '/certificates',
    name: 'Certificates',
    component: Certificates
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
