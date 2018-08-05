<template>
	<div>
		<div>
			<v-icon class = "mr-1" > mdi-comment </v-icon>
			<span style = "font-size:20px;font-weight:500;" > Comments: </span>
		</div>

		<div style = "width:auto">
			<comments v-model = "data" />
		</div>

		<div
			:class="{'mb-2': $vuetify.breakpoint.xsOnly}"
			class="text-xs-center mt-2">
			<v-pagination
				ref = "pagination"
				v-model = "page"
				:length = "maxpage"/>
		</div>

	</div>
</template>


<script>

import comments from '@/components/comments/comments';
import CommentsGQL from '@/graphql/blog/discussion.gql';

export default {

	components: {
		comments,
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
		request(force = false) {
			this.$apollo.query({
				query: CommentsGQL,
				variables: {
					slug: this.slug,
					page: this.page,
					time: force ? Date.now() : 0,
				},
			})
				.then(response => response.data.blogDiscussionList)
				.then((data) => {
					this.maxpage = data.maxpage;
					this.page = Math.min(this.page, this.maxpage);
					this.data = data.discussionList;
				});
		},
	},

};
</script>
