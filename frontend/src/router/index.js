import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/home/home.vue'
import Login from '@/components/signin/login.vue'
import Signup from '@/components/signin/signup.vue'
import Signout from '@/components/signin/signout.vue'
import NotFound from '@/components/global/404.vue'
import ProblemList from '@/components/problem/app.vue'
import ProblemDetail from '@/components/problem/detail/app.vue'
import ProblemDescription from '@/components/problem/detail/description.vue'
import ProblemEditor from '@/components/problem/detail/editor.vue'
import ProblemDiscussion from '@/components/problem/detail/discussion.vue'

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
      path: '/signout',
      name: 'Signout',
      component: Signout
    },

    {
      path: '/problemlist',
      name: 'ProblemList',
      component: ProblemList
    },

    {
      path: '/problem/:slug',
      component: ProblemDetail,
      children:
      [
        {
          path: '',
          name: 'ProblemDetail',
          component: ProblemDetail
        },
        {
          path: 'description',
          name: 'ProblemDetailDescription',
          component: ProblemDescription
        },
        {
          path: 'editor',
          name: 'ProblemDetailEditor',
          component: ProblemEditor
        },
        {
          path: 'discussion',
          name: 'ProblemDetailDiscussion',
          component: ProblemDiscussion
        }
      ]
    },

    {
      path : '*',
      name : '404',
      component: NotFound
    }

  ]
})
