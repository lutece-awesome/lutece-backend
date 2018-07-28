/* eslint no-shadow: ["error", { "allow": ["state"] }] */
import { RefreshToken } from '@/graphql/signin/token.gql';
import jwtDecode from 'jwt-decode';
import apolloProvider from '@/apollo';

const state = {
	payload: null,
	permission: [],
};

const getters = {
	has_permission: state => permission => state.permission.indexOf(permission) !== -1,
};

const mutations = {
	login(state, data) {
		state.payload = data.payload;
		state.permission = JSON.parse(data.permission);
		localStorage.setItem('USER_TOKEN', data.token);
	},
	logout(state) {
		state.payload = null;
		state.permission = [];
		localStorage.removeItem('USER_TOKEN');
	},
};

const actions = {
	refresh_token({ commit }, force) {
		const BEFORE_EXPIRATION_DELTA = 60 * 60;
		const token = localStorage.getItem('USER_TOKEN');
		if (token) {
			const decoded = jwtDecode(token);
			const now = Date.now() / 1000;
			if (decoded.exp <= now) {
				commit('logout');
			} else if (force || decoded.exp - now < BEFORE_EXPIRATION_DELTA) {
				apolloProvider.defaultClient.mutate({
					mutation: RefreshToken,
					variables: {
						token,
					},
				})
					.then(response => response.data.refreshToken)
					.then((data) => {
						commit('login', data);
					})
					.catch((error) => {
						commit('snackbar/setSnack', error.message, { root: true });
						commit('logout');
					});
			}
		}
	},
};

export default {
	namespaced: true,
	getters,
	state,
	mutations,
	actions,
};
