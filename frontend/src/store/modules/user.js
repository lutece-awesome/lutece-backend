/* eslint no-shadow: ["error", { "allow": ["state"] }] */
import { RefreshToken } from '@/graphql/signin/token.gql';
import jwtDecode from 'jwt-decode';
import apolloProvider from '@/apollo';

const state = {
	authed: false,
	displayname: '',
	gravataremail: '',
};

const getters = {
	authed: state => state.authed,
};

const mutations = {
	login(state, data) {
		state.authed = true;
		state.gravataremail = data.payload.gravataremail;
		state.displayname = data.payload.displayname;
		localStorage.setItem('USER_TOKEN', data.token);
	},
	logout(state) {
		state.authed = false;
		state.gravataremail = '';
		state.displayname = '';
		localStorage.removeItem('USER_TOKEN');
	},
};

const actions = {
	refresh_token({ commit }) {
		const token = localStorage.getItem('USER_TOKEN');
		if (token) {
			const decoded = jwtDecode(token);
			if (decoded.exp <= Date.now() / 1000) {
				commit('logout');
			} else {
				apolloProvider.defaultClient.mutate({
					mutation: RefreshToken,
					variables: {
						token,
					},
				})
					.then(response => response.data.refreshToken)
					.then((data) => {
						commit('login', data);
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
