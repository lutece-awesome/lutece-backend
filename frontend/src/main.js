import 'babel-polyfill';
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import {
	Vuetify, // required
	VApp, // required
	VSwitch,
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
	VProgressLinear,
	VSnackbar,
	transitions,
} from 'vuetify';
import { Resize } from 'vuetify/es5/directives';
import colors from 'vuetify/es5/util/colors';
import Meta from 'vue-meta';
import lineClamp from 'vue-line-clamp';
import router from './router';
import Base from './base';
import apolloProvider from './apollo';
import store from './store';
import mixrend from '@/plugins/markdown-it-katex';

import '@mdi/font/css/materialdesignicons.css';
import 'katex/dist/katex.css';
import './stylus/main.styl';

Vue.use(require('vue-moment'));

Vue.config.productionTip = false;
Vue.use(Meta);
Vue.use(mixrend);
Vue.use(lineClamp);
Vue.use(Vuetify, {
	components: {
		VSwitch,
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
		VProgressLinear,
		VSnackbar,
		transitions,
	},
	directives: {
		Resize,
	},
	iconfont: 'mdi',
	theme: {
		primary: colors.blue.darken1,
		secondary: colors.blue.darken2,
		accent: colors.pink.base,
	},
});

Vue.filter('nl2br', text => text.replace(/(?:\r\n|\r|\n)/g, '<br>'));

/* eslint-disable no-new */
new Vue({
	el: '#app',
	provide: apolloProvider.provide(),
	router,
	store,
	components: { Base },
	data() {
		return {
			title: 'Lutece',
		};
	},
	watch: {
		$route(to) {
			if (to.name !== 'Signout') {
				this.$store.dispatch('user/refresh_token');
			}
		},
	},
	created() {
		this.$store.dispatch('user/refresh_token', true);
	},
	template: '<Base/>',
});
