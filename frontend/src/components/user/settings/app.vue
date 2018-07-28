<template>
	<v-container v-if = "!isloading">
		<v-layout
			justify-center
			row
			wrap>
			<v-flex
				xs12
				md6>
				<v-form>
					<v-text-field
						v-model="displayName"
						label="Display name"
					/>
				</v-form>
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>

import UserProfileGQL from '@/graphql/user/settings.gql';

export default {
	data: () => ({
		displayName: '',
		school: '',
		company: '',
		location: '',
		about: '',
		group: '',
		isloading: false,
	}),
	mounted() {
		this.request();
	},
	methods: {
		request() {
			this.isloading = true;
			this.$apollo.query({
				query: UserProfileGQL,
				variables: {
					username: this.$store.state.user.payload.username,
				},
			})
				.then(response => response.data.user)
				.then((data) => { this.data = data; })
				.finally(() => { this.isloading = false; });
		},
	},
};
</script>
