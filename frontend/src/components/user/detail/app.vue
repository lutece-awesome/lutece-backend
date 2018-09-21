<template>
	<div>
		<v-btn
			v-if = "$store.state.user.payload && username == $store.state.user.payload.username"
			:to = "{name: 'UserSettings'}"
			color = "accent"
			dark
			fab
			fixed
			bottom
			right>
			<v-icon>mdi-pencil</v-icon>
		</v-btn>
		<v-container>
			<v-layout
				row
				justify-center
				wrap>
				<v-flex
					xs12
					sm11
					md10
				>
					<ApolloQuery
						:query = "require('@/graphql/user/profile.gql')"
						:variables = "{ username }"
					>
						<template
							slot-scope = "{ result: { loading , error , data } }">
							<LoadingSpinner v-if = "loading" />
							<div v-else-if = "error" >An error occured</div>
							<div v-else-if = "data">
								<Layout :user = "data.user"/>
							</div>
						</template>
					</ApolloQuery>
				</v-flex>
			</v-layout>
		</v-container>
	</div>
</template>


<script>

import LoadingSpinner from '@/components/basic/loading';
import Layout from '@/components/user/detail/layout';

export default {
	metaInfo() { return { title: this.username }; },

	components: {
		LoadingSpinner,
		Layout,
	},

	computed: {
		username() {
			return this.$route.params.username;
		},
		isxs() {
			return this.$vuetify.breakpoint.smAndDown;
		},
		notxs() {
			return !this.$vuetify.breakpoint.smAndDown;
		},
	},
};
</script>
