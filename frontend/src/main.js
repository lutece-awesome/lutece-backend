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
	VForm,
	VDivider,
	transitions,
} from 'vuetify';
import { Ripple, Resize } from 'vuetify/es5/directives';
import colors from 'vuetify/es5/util/colors';
import Meta from 'vue-meta';
import router from './router';
import Base from './base';
import apolloProvider from './apollo';
import store from './store';
import mixrend from '@/plugins/markdown-it-katex';
import '@mdi/font/css/materialdesignicons.css';
import 'katex/dist/katex.css';
import './stylus/main.styl';

Vue.config.productionTip = false;
Vue.use(Meta);
Vue.use(mixrend);
Vue.use(require('vue-moment'));

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
		VForm,
		VDivider,
		transitions,
	},
	directives: {
		Ripple,
		Resize,
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
