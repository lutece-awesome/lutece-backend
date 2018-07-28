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
						v-model="payload.displayname"
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
		payload: {},
	}),
	created() {
		this.updatePayload();
		this.$store.watch(state => state.user.payload, this.updatePayload);
	},
	methods: {
		updatePayload() {
			this.payload = Object.assign({}, this.$store.state.user.payload);
		},
	},
};
</script>
