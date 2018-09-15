/* eslint no-shadow: ["error", { "allow": ["state"] }] */

export const state = () => ({
	visible: false,
});

export const mutations = {
	setVisible(state, visible) {
		state.visible = (visible === true);
	},
};

const getters = {
	visible: state => state.visible,
};

export default {
	namespaced: true,
	state,
	getters,
	mutations,
};
