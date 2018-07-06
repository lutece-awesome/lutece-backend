

const state = {
    'authed': false,
    'gravataremail' : null,
}

const getters = {
    has_authed: ( state )=>{
        return state.authed;
    },
}

const mutations = {
    set_authed( state ){
        state.authed = true;
    },
    set_unthed( state ){
        state.authed = false;
    },
    set_gravataremail( state , email ){
        state.gravataremail = email;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations
}