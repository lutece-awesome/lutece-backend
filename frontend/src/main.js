import 'babel-polyfill';
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuetify from 'vuetify';
import colors from 'vuetify/es5/util/colors';
import router from './router';
import Base from './base';
import apolloProvider from './apollo';
import store from './store';
import VueKatex from '@/plugins/katex';
import 'vuetify/dist/vuetify.min.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import '@mdi/font/css/materialdesignicons.css';

Vue.config.productionTip = false;
Vue.use(VueKatex);
Vue.use(Vuetify, {
	theme: {
		primary: colors.blue.darken1,
		secondary: colors.blue.darken2,
		accent: colors.pink.base,
	},
});

/* eslint-disable no-new */
new Vue({
	el: '#app',
	provide: apolloProvider.provide(),
	router,
	store,
	components: { Base },
	template: '<Base/>',
});
