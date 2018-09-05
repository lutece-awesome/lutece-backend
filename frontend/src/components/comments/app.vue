<template>
	<div>
		<div>
			<v-icon class = "mr-1" > mdi-comment </v-icon>
			<span style = "font-size:20px;font-weight:500;" > Comments: </span>
		</div>

		<ApolloQuery
			:query = "require('@/graphql/blog/discussion.gql')"
			:variables = "{ page , slug }"
			@result = "onResult" >
			<template
				slot-scope = "{ result: { loading , error , data } }">
				<LoadingSpinner v-if = "loading" />
				<div v-else-if = "error" > An error occured </div>
				<div v-else-if = "data">
					<comments v-model = "data.blogDiscussionList.blogDiscussionList" />
					<div
						:class = "{'mb-2': $vuetify.breakpoint.xsOnly}"
						class = "text-xs-center mt-2">
						<v-pagination
							ref = "pagination"
							v-model = "page"
							:length = "data.blogDiscussionList.maxpage"/>
					</div>
				</div>
			</template>
		</ApolloQuery>

	</div>
</template>


<script>

import comments from '@/components/comments/comments';
import LoadingSpinner from '@/components/basic/loadingspinner';

export default {

	components: {
		comments,
		LoadingSpinner,
	},

	props: {
		slug: {
			type: String,
			required: true,
		},
	},

	data: () => ({
		data: null,
		page: 1,
		maxpage: 0,
		isLoading: false,
	}),

	watch: {
		page() {
			this.request();
		},
	},

	activated() {
		this.$refs.pagination.init();
		this.request();
	},

	mounted() {
		this.request();
	},

	methods: {

		onResult(result) {
			this.maxpage = result.data.blogDiscussionList.maxpage;
		},

	},

};
</script>
