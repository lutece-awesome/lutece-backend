import 'babel-polyfill';
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import {
	Vuetify, // required
	VApp, // required
	VNavigationDrawer,
	VGrid,
	VToolbar,
	VList,
	VBtn,
	VAvatar,
	VCard,
	VMenu,
	VIcon,
	VAutocomplete,
	VDataTable,
	VPagination,
	VTabs,
	VSelect,
	VTextField,
	transitions,
} from 'vuetify';
import { Ripple } from 'vuetify/es5/directives';
import colors from 'vuetify/es5/util/colors';
import router from './router';
import Base from './base';
import apolloProvider from './apollo';
import store from './store';
import mixrend from '@/plugins/markdown-it-katex';
import '@mdi/font/css/materialdesignicons.css';
import 'katex/dist/katex.min.css';

require('vuetify/src/stylus/app.styl');

Vue.config.productionTip = false;
Vue.use(mixrend);
Vue.use(Vuetify, {
	components: {
		VApp,
		VNavigationDrawer,
		VGrid,
		VToolbar,
		VList,
		VBtn,
		VAvatar,
		VCard,
		VMenu,
		VIcon,
		VAutocomplete,
		VDataTable,
		VPagination,
		VTabs,
		VSelect,
		VTextField,
		transitions,
	},
	directives: {
		Ripple,
	},
	iconfont: 'mdi',
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
