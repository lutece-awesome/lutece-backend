
<template>
	<v-layout justify-center>
		<v-flex
			xs12
			sm8
			md6
			xl4>
			<v-card>
				<v-card-title>
					<v-layout
						justify-center
						mt-3>
						<span class="headline">SIGN UP</span>
					</v-layout>
				</v-card-title>
				<v-card-text>
					<v-form @submit.prevent="register">
						<v-layout column>
							<v-flex>
								<v-text-field
									v-model="username"
									:error-messages="geterror('username')"
									label="Username *"
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
									label="Email *"
									required />
							</v-flex>
							<v-flex>
								<v-text-field
									v-model="displayname"
									:error-messages="geterror('displayname')"
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
			displayname: '',
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
					displayname: this.displayname,
					school: this.school,
					company: this.company,
					location: this.location,
				},
			})
				.then(response => response.data.Register)
				.then((data) => {
					this.aftersignup(data.token);
				})
				.catch((error) => {
					this.error = true;
					this.errordetail = JSON.parse(error.graphQLErrors[0].message);
				})
				.finally(() => { this.loading = false; });
		},

		aftersignup(token) {
			Object.values(this.$apollo.provider.clients)
				.forEach(client => client.cache.reset());
			localStorage.setItem('USER_TOKEN', token);
			this.$store.commit('user/update_authed', true);
			this.$router.push({
				name: 'Home',
			});
		},
	},
};
</script>
