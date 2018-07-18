<!--
    Homepage
-->
<template>
	<div
		:class="{'pa-3': $vuetify.breakpoint.xsOnly }">
		<h1 class="display-3">Lutece</h1>

		<span class="display-1">Meet the future</span>

		<v-divider class="my-3"/>
		<v-btn
			class="mx-0"
			color="primary"
			large
			href="https://github.com/LaPluses/Lutece"
		>
			<v-icon
				left
				dark>mdi-github-circle</v-icon>
			Github
		</v-btn>
	</div>

</template>

<script>
export default {
	metaInfo() { return { title: 'Home' }; },
};
</script>
