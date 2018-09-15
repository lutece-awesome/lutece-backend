import Vue from 'vue';
import Vuex from 'vuex';
import user from './modules/user';
import snackbar from './modules/snackbar';
import navbar from './modules/navbar';
import footer from './modules/footer';


Vue.use(Vuex);

export default new Vuex.Store({
	modules: {
		user,
		snackbar,
		navbar,
		footer,
	},
});
