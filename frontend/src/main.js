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

Vue.config.productionTip = false
Vue.use(Vuetify)

/* eslint-disable no-new */
new Vue({
  el: '#Lutece',
  provide: apolloProvider.provide(),
  router,
  store,
  components: { Base },
  template: '<Base/>'
})