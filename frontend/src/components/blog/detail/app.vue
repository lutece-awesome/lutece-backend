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
				<div class = "display-2 text-xs-center mt-2">
					{{ blog.title }}
				</div>
				<div
					class = "text-xs-center mt-2"
					style = "color:#999;"
				>
					<span> {{ blog.createTime | moment("MMMM Do, YYYY") }} </span>
					<span style = "margin-left:4px;margin-right:4px;" > | </span>
					<span> {{ blog.view }} views </span>
					<span style = "margin-left:4px;margin-right:4px;" > | </span>
					<span>
						{{ blog.vote }} stars
						<v-icon style = "margin-left:4px;">mdi-thumb-up-outline </v-icon>
					</span>
				</div>

				<v-divider class="my-3"/>
				<div
					class="subheading">
					{{ blog.content }}
				</div>
				<v-divider class="my-3"/>

				<Commtents/>

				<!-- <div>
					view: {{ blog.view }}
				</div>

				<div>
					vote: {{ blog.vote }}
				</div> -->
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>
import BlogGQL from '@/graphql/blog/detail.gql';
import Commtents from '@/components/blog/basic/comments';

export default {

	components: {
		Commtents,
	},

	data: () => ({
		slug: '',
		blog: {
			title: '',
			content: '',
			view: 0,
			vote: 0,
			createTime: '',
		},
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
