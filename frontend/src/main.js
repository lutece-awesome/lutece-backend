import '@babel/polyfill';
import Vue from 'vue';
import '@mdi/font/css/materialdesignicons.css';
import 'katex/dist/katex.css';
import './plugins/filters';
import './plugins/markdown-it-katex';
import './plugins/vue-line-clamp';
import './plugins/vue-meta';
import './plugins/vue-moment';
import './plugins/vuetify';
import App from './App';
import router from './router';
import store from './store';
import apolloProvider from './apollo';
import './registerServiceWorker';
import './stylus/main.styl';

Vue.config.productionTip = false;

new Vue({
	router,
	store,
	provide: apolloProvider.provide(),
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
	render: h => h(App),
}).$mount('#app');
