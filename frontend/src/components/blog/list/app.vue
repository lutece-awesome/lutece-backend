<template>
	<v-container
		fluid>
		<v-layout
			row
			justify-center>
			<v-flex
				xs10
				md8
				lg6>
				<ApolloQuery
					:query = "require('@/graphql/blog/list.gql')"
					:variables = "{ page }"
					@result = "onResult" >
					<template
						slot-scope = "{ result: { loading , error , data } }">
						<div
							v-if = "loading"
						> Loading... </div>
						<div
							v-else-if = "error"
						>An error occured</div>
						<BlogList
							v-else-if = "data"
							:items = "data.blogList.blogList"
						/>
					</template>
				</ApolloQuery>
				<div
					:class="{'mb-2': $vuetify.breakpoint.xsOnly}"
					class="text-xs-center mt-2">
					<v-pagination
						ref = "pagination"
						v-model = "page"
						:length = "maxpage"/>
				</div>
				<v-btn
					v-if = "this.$store.getters['user/isAuthenticated']"
					:to="{name: 'BlogCreate'}"
					color="accent"
					dark
					fab
					fixed
					bottom
					right>
					<v-icon>mdi-pencil</v-icon>
				</v-btn>
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>
import BlogList from '@/components/blog/list/list';

export default {
	name: 'Blog',
	metaInfo() { return { title: 'Blog' }; },

	components: {
		BlogList,
	},

	data: () => ({
		page: 1,
		maxpage: 0,
	}),

	activated() {
		this.$refs.pagination.init();
	},

	methods: {
		onResult(result) {
			this.maxpage = result.data.blogList.maxpage;
		},
	},
};
</script>
