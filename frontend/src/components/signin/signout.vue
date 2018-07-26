<template>
	<div/>
</template>

<script>
export default {
	created() {
		this.$store.commit('user/logout');
		this.$apollo.provider.defaultClient.resetStore().then(() => {
			this.$router.push(this.$route.query.redirect || '/');
		});
	},
};
</script>
