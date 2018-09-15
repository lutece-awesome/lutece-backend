/* eslint no-shadow: ["error", { "allow": ["state"] }] */

export const state = () => ({
	visible: true,
});

export const mutations = {
	setVisible(state, visible) {
		state.visible = (visible === true);
	},
};

const getters = {
	visible: state => state.visible,
};

const actions = {
	setVisible({ flag, commit }) {
		commit('setVisible', flag);
	},
};

export default {
	namespaced: true,
	state,
	actions,
	getters,
	mutations,
};
