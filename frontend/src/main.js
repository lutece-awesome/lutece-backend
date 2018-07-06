// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import Base from './components/base'
import apolloProvider from './apollo.js'
import store from './store'
import '../semantic/dist/semantic.min.css'
import '../semantic/dist/semantic.min.js'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#Lutece',
  provide: apolloProvider.provide(),
  router,
  components: { Base },
  template: '<Base/>'
})