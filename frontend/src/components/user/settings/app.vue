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
						v-model="displayname"
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

import { UserInfoUpdateGQL } from '@/graphql/user/settings.gql';

export default {
	metaInfo() { return { title: 'Settings' }; },

	data: () => ({
		displayname: '',
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
		this.displayname = this.$store.state.user.displayname;
		this.school = this.$store.state.user.school;
		this.company = this.$store.state.user.company;
		this.location = this.$store.state.user.location;
		this.about = this.$store.state.user.about;
		this.group = this.$store.state.user.group;
	},
	methods: {
		geterror(field) {
			if (Object.prototype.hasOwnProperty.call(this.errordetail, field)) {
				return this.errordetail[field][0].message;
			}
			return '';
		},


		submit() {
			this.isloading = true;
			this.errordetail = [];
			this.error = false;
			this.$apollo.mutate({
				mutation: UserInfoUpdateGQL,
				variables: {
					company: this.company,
					displayname: this.displayname,
					about: this.about,
					school: this.school,
					location: this.location,
				},
			})
				.then(() => {
					this.$store.dispatch('user/refresh_token', true);
					this.$router.push({
						name: 'UserDetail',
						params: { username: this.$store.state.user.payload.username },
					});
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
