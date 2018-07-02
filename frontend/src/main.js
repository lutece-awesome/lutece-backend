// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import Base from './components/base'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#Lutece',
  router,
  components: { Base },
  template: '<Base/>'
})