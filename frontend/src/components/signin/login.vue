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
						<v-form @submit.prevent="login">
							<v-layout column>
								<v-flex>
									<v-text-field
										v-model="username"
										:error-messages="geterror('username')"
										label="Username"
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
										type="submit">Login</v-btn>
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

export default {
	metaInfo() { return { title: 'Login' }; },
	data: () => ({
		loading: false,
		error: false,
		username: '',
		password: '',
		errordetail: {},
	}),

	methods: {
		geterror(field) {
			if (Object.prototype.hasOwnProperty.call(this.errordetail, field)) {
				return this.errordetail[field][0].message;
			}
			return '';
		},

		login() {
			this.loading = true;
			this.error = false;
			this.errordetail = {};
			const { username, password } = this;
			this.$store.dispatch('user/login', { username, password })
				.then(() => {
					this.$router.push(this.$route.query.redirect || '/');
				})
				.catch((error) => {
					this.errordetail = JSON.parse(error.graphQLErrors[0].message);
					this.error = true;
				})
				.finally(() => { this.loading = false; });
		},

		redirect() {
		},

		signup() {
			this.$router.push({
				name: 'Signup',
				query: {
					redirect: this.$route.query.redirect || '/',
				},
			});
		},
	},
};
</script>
