import { createRouter, createWebHistory } from 'vue-router';
import OneView from './components/OneView';
import Login from './components/Login';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'Home',
      path: '/home',
      component: OneView
    },
    {
      name: 'Login',
      path: '/login',
      component: Login
    }
  ],
});

export default router;