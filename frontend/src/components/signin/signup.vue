
<template>
	<v-container
		:class="{'pa-0': $vuetify.breakpoint.xsOnly }"
		fluid>
		<v-layout justify-center>
			<v-flex
				xs12
				sm8
				md6
				xl4>
				<v-card>
					<v-card-text>
						<v-form @submit.prevent="register">
							<v-layout column>
								<v-flex>
									<v-text-field
										v-model="username"
										:error-messages="geterror('username')"
										label="Username *"
										autocomplete="off"
										autocorrect="off"
										autocapitalize="off"
										spellcheck="false"
										required />
								</v-flex>
								<v-flex>
									<v-text-field
										v-model="password"
										:error-messages="geterror('password')"
										type="password"
										label="Password *"
										required />
								</v-flex>
								<v-flex>
									<v-text-field
										v-model="email"
										:error-messages="geterror('email')"
										type="email"
										label="Email *"
										required />
								</v-flex>
								<v-flex>
									<v-text-field
										v-model="displayName"
										:error-messages="geterror('displayName')"
										label="Display name *"
										required />
								</v-flex>
								<v-flex>
									<v-text-field
										v-model="school"
										:error-messages="geterror('school')"
										label="School" />
								</v-flex>
								<v-flex>
									<v-text-field
										v-model="company"
										:error-messages="geterror('company')"
										label="Company" />
								</v-flex>
								<v-flex>
									<v-text-field
										v-model="location"
										:error-messages="geterror('location')"
										label="Location" />
								</v-flex>
								<v-flex mt-3>
									<v-btn
										:loading="loading"
										:color="error ? &quot;error&quot; : &quot;primary&quot;"
										block
										big
										type="submit">Register</v-btn>
								</v-flex>
							</v-layout>
						</v-form>
					</v-card-text>
				</v-card>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
import RegisterGQL from '@/graphql/signin/register.gql';

export default {
	metaInfo() { return { title: 'Sign Up' }; },
	data() {
		return {
			username: '',
			password: '',
			email: '',
			displayName: '',
			school: '',
			company: '',
			location: '',
			loading: false,
			error: false,
			errordetail: {},
		};
	},

	methods: {

		geterror(field) {
			if (Object.prototype.hasOwnProperty.call(this.errordetail, field)) {
				return this.errordetail[field][0].message;
			}
			return '';
		},

		register() {
			this.errordetail = {};
			this.error = false;
			this.loading = true;
			this.$apollo.mutate({
				mutation: RegisterGQL,
				variables: {
					username: this.username,
					password: this.password,
					email: this.email,
					displayName: this.displayName,
					school: this.school,
					company: this.company,
					location: this.location,
				},
			})
				.then(response => response.data.Register)
				.then((data) => {
					this.$store.commit('user/login', data);
					this.$apollo.provider.defaultClient.resetStore().then(() => {
						this.$router.push(this.$route.query.redirect || '/');
					});
				})
				.catch((error) => {
					this.error = true;
					this.errordetail = JSON.parse(error.graphQLErrors[0].message);
				})
				.finally(() => { this.loading = false; });
		},
	},
};
</script>
