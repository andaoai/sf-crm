import { createRouter, createWebHistory } from 'vue-router'
import Companies from '../views/Companies.vue'
import Talents from '../views/Talents.vue'
import Communications from '../views/Communications.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
