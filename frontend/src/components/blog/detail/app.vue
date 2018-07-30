<template>
	<v-container>
		<v-layout
			row
			wrap
			justify-center
		>
			<v-flex
				xs12
				md8>
				<div
					class = "display-2"
					style = "text-align:center;" > {{ blog.title }} </div>
				<div
					class="subheading">
					{{ blog.content }}
				</div>

				<div>
					view: {{ blog.view }}
				</div>

				<div>
					vote: {{ blog.vote }}
				</div>
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>
import BlogGQL from '@/graphql/blog/detail.gql';

export default {
	data: () => ({
		slug: '',
		blog: null,
	}),
	mounted() {
		this.slug = this.$route.params.slug;
		this.request();
	},

	methods: {
		request() {
			this.$apollo.query({
				query: BlogGQL,
				variables: {
					slug: this.slug,
				},
			})
				.then(response => response.data.blog)
				.then((data) => { this.blog = data; });
		},
	},
};
</script>
