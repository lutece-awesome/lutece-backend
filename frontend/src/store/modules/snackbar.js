/* eslint no-shadow: ["error", { "allow": ["state"] }] */

export const state = () => ({
	snack: '',
});

export const mutations = {
	setSnack(state, snack) {
		state.snack = snack;
	},
};

export default {
	namespaced: true,
	state,
	mutations,
};
