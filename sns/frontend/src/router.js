import { createRouter, createWebHistory } from 'vue-router';
import Index from './components/Index';
import Login from './components/Login';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'INdex',
      path: '/home',
      component: Index
    },
    {
      name: 'Login',
      path: '/login',
      component: Login
    }
  ],
});

export default router;