<template>
	<v-container>
		<v-layout
			justify-center
			row
			wrap>
			<v-flex
				xs12
				md6>
				<v-form>
					<v-text-field
						v-model="displayname"
						label="Display name"
					/>
				</v-form>
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>
export default {
	data: () => ({
		displayname: '',
	}),

	mounted() {
		this.displayname = this.$store.state.user.displayname;
	},
};
</script>
