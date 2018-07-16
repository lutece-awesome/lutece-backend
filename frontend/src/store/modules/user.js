/* eslint no-shadow: ["error", { "allow": ["state"] }] */
const state = {
	displayname: '',
	gravataremail: '',
	authed: false,
};

const mutations = {
	update_authed(state, flag) {
		state.authed = flag;
	},
	update_gravataremail(state, email) {
		state.gravataremail = email;
	},
	update_displayname(state, displayname) {
		state.displayname = displayname;
	},
};

export default {
	namespaced: true,
	state,
	mutations,
};
