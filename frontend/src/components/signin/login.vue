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
						<span class="headline">SIGN IN</span>
					</v-layout>
				</v-card-title>
				<v-card-text>
					<form>
						<v-layout column>
							<v-flex>
								<v-text-field
									v-model="username"
									:error-messages="geterror('username')"
									label="Username"
									required />
							</v-flex>
							<v-flex>
								<v-text-field
									v-model="password"
									:error-messages="geterror('password')"
									type="password"
									label="Password"
									required />
							</v-flex>
							<v-flex>
								<a @click="signup">Do not have account? </a>
							</v-flex>
							<v-flex
								class="text-xs-center"
								mt-3>
								<v-btn
									:loading = "loading"
									:color="error ? &quot;error&quot; : &quot;primary&quot;"
									block
									big
									@click="login">Login</v-btn>
							</v-flex>
						</v-layout>
					</form>
				</v-card-text>
			</v-card>
		</v-flex>
	</v-layout>
</template>

<script>
import { UserLogin } from '@/graphql/signin/token.gql';

export default {
	data: () => ({
		loading: false,
		error: false,
		username: '',
		password: '',
		errordetail: {},
	}),

	methods: {
		geterror(field) {
			if (this.errordetail.hasOwnProperty.call(field)) {
				return this.errordetail[field][0].message;
			}
			return '';
		},

		login() {
			this.loading = true;
			this.error = false;
			this.errordetail = {};
			this.$apollo
				.mutate({
					mutation: UserLogin,
					variables: {
						username: this.username,
						password: this.password,
					},
				})
				.then(response => response.data.UserLogin)
				.then((data) => {
					localStorage.setItem('USER_TOKEN', data.token);
					this.$store.commit('user/update_authed', true);
					this.redirect();
				})
				.catch((error) => {
					this.errordetail = JSON.parse(error.graphQLErrors[0].message);
					this.error = true;
				})
				.finally(() => { this.loading = false; });
		},

		redirect() {
			Object.values(this.$apollo.provider.clients).forEach(client => client.cache.reset());
			this.$router.push(this.$route.query.redirect || '/');
		},

		signup() {
			this.$router.push({
				name: 'Signup',
			});
		},
	},
};
</script>
