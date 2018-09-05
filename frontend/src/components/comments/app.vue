<template>
	<div>
		<div class = "mb-3">
			<v-icon class = "mdi-20px" > mdi-comment </v-icon>
			<span class = "title ml-1" > Comments: </span>
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
					<Comments v-model = "data.blogDiscussionList.discussionList" />
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

import Comments from '@/components/comments/comments';
import LoadingSpinner from '@/components/basic/loadingspinner';

export default {

	components: {
		Comments,
		LoadingSpinner,
	},

	props: {
		slug: {
			type: String,
			required: true,
		},
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
			this.maxpage = result.data.blogDiscussionList.maxpage;
		},

	},

};
</script>
