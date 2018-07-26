<template>

	<v-layout
		row
		justify-center>
		<v-flex
			xs12
			md8>
			<v-card>
				<v-card-title primary-title>
					<h3 class="headline">{{ username }}</h3>
				</v-card-title>
			</v-card>
		</v-flex>
	</v-layout>

</template>


<script>

export default {
	metaInfo() { return { title: this.username }; },
	data: () => ({
		username: '',
	}),

	mounted() {
		this.username = this.$route.params.username;
	},
};
</script>
