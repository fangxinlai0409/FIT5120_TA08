import { createRouter, createWebHistory } from 'vue-router'

import UvPage from '../views/UvPage.vue'
import ProtectionPage from '../views/ProtectionPage.vue'
import NewsPage from '../views/NewsPage.vue'

const routes = [
  { path: '/', redirect: '/uv' },
  { path: '/uv', name: 'uv', component: UvPage },
  { path: '/protection', name: 'protection', component: ProtectionPage },
  { path: '/news', name: 'news', component: NewsPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
