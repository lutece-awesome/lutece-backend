<template>
	<div/>
</template>

<script>
export default {
	created() {
		this.$store.dispatch('user/logout').then(() => {
			this.$router.push(this.$route.query.redirect || '/');
		});
	},
};
</script>
