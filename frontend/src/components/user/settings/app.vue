<template>
	<v-container v-if = "!initialize">
		<v-layout
			justify-center
			row
			wrap>
			<v-flex
				xs12
				md6>
				<v-form
					@submit.prevent="submit"
				>
					<v-text-field
						v-model="displayName"
						:error-messages="geterror('displayname')"
						label="Display name"
						prepend-icon = "mdi-account"
					/>
					<v-text-field
						v-model="group"
						:error-messages="geterror('group')"
						label="Group"
						prepend-icon = "mdi-account-group"
						disabled
					/>
					<v-text-field
						v-model="school"
						:error-messages="geterror('school')"
						label="School"
						prepend-icon = "mdi-school"
					/>
					<v-text-field
						v-model="company"
						:error-messages="geterror('company')"
						label="Company"
						prepend-icon = "mdi-briefcase"
					/>
					<v-text-field
						v-model="location"
						:error-messages="geterror('location')"
						label="Location"
						prepend-icon = "mdi-map-marker"
					/>

					<v-textarea
						v-model="about"
						:error-messages="geterror('about')"
						label="About"
						auto-grow
					/>

					<v-btn
						:loading = "isloading"
						:color="error ? &quot;error&quot; : &quot;primary&quot;"
						block
						type = "submit"
					> Submit </v-btn>
				</v-form>
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>

import { UserProfileGQL, UserInfoUpdateGQL } from '@/graphql/user/settings.gql';

export default {
	metaInfo() { return { title: 'Settings' }; },

	data: () => ({
		displayName: '',
		school: '',
		company: '',
		location: '',
		about: '',
		group: '',
		isloading: false,
		initialize: false,
		error: false,
		errordetail: [],
	}),
	mounted() {
		this.request();
	},
	methods: {
		geterror(field) {
			if (Object.prototype.hasOwnProperty.call(this.errordetail, field)) {
				return this.errordetail[field][0].message;
			}
			return '';
		},

		request() {
			this.initialize = true;
			this.$apollo.query({
				query: UserProfileGQL,
			})
				.then(response => response.data.user)
				.then((data) => { Object.assign(this, data); })
				.finally(() => { this.initialize = false; });
		},

		submit() {
			this.isloading = true;
			this.errordetail = [];
			this.error = false;
			this.$apollo.mutate({
				mutation: UserInfoUpdateGQL,
				variables: {
					company: this.company,
					displayname: this.displayName,
					about: this.about,
					school: this.school,
					location: this.location,
				},
			})
				.finally(() => { this.isloading = false; })
				.catch((error) => {
					this.errordetail = JSON.parse(error.graphQLErrors[0].message);
					this.error = true;
				});
		},
	},
};
</script>
