import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/home/home.vue'
import Login from '@/components/signin/login.vue'
import NotFound from '@/components/basic/404.vue'

Vue.use(Router)

export default new Router({
  mode : 'history',
  routes: [

    {
      path: '',
      redirect:{
        name : 'Home'
      }
    },

    {
      path: '/home',
      name: 'Home',
      component: Home
    },

    {
      path : '/login$',
      name : 'Login',
      component: Login
    },


    {
      path : '*',
      name : '404',
      component: NotFound
    }

  ]
})
