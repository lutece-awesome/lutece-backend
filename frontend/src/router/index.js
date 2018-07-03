import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/home/home.vue'
import Login from '@/components/signin/login.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'Home',
      component: Home
    },

    {
      path : '/login',
      name : 'Login',
      component: Login
    }

  ]
})
