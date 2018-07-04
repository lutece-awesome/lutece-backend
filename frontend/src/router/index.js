import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/home/home.vue'
import Login from '@/components/signin/login.vue'
import Signup from '@/components/signin/signup.vue'
import NotFound from '@/components/basic/404.vue'
import ProblemList from '@/components/problem/list.vue'

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
      path : '/login',
      name : 'Login',
      component: Login
    },

    {
      path: '/signup',
      name: 'Signup',
      component: Signup
    },

    {
      path: '/problem',
      name : 'Problem',
      component: ProblemList
    },

    {
      path : '*',
      name : '404',
      component: NotFound
    }

  ]
})
