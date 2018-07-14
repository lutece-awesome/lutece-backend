// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import Base from './base'
import apolloProvider from './apollo.js'
import store from './store'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'
import colors from 'vuetify/es5/util/colors'

Vue.config.productionTip = false
Vue.use(Vuetify, {
  theme: {
    primary: colors.teal.darken1,
    secondary: colors.teal.lighten4,
    accent: colors.pink.base
  }
})
 
/* eslint-disable no-new */
new Vue({
  el: '#Lutece',
  provide: apolloProvider.provide(),
  router,
  store,
  components: { Base },
  template: '<Base/>'
})