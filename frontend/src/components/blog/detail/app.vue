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
					<div> Created by
						<router-link :to = "{name: 'UserDetail', params: {username: blog.user.username}}" >
							{{ blog.user.displayName }}
						</router-link>
					</div>
					<span> {{ blog.createTime | moment("MMMM Do, YYYY") }} </span>
					<span class = "ml-1 mr-1" > | </span>
					<span> {{ blog.view }} views </span>
					<span class = "ml-1 mr-1" > | </span>
					<span>
						{{ blog.vote }} stars
						<v-icon class = "ml-1" >mdi-thumb-up-outline </v-icon>
					</span>
				</div>

				<v-divider class="my-3"/>
				<div
					v-mixrend = "blog.content"
					class="subheading"/>
				<v-divider class="my-3"/>

				<Commtents
					:slug = "slug"
				/>
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>
import BlogGQL from '@/graphql/blog/detail.gql';
import Commtents from '@/components/comments/app';

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
			user: {
				username: '',
				displayName: '',
			},
		},
	}),

	created() {
		this.slug = this.$route.params.slug;
	},

	mounted() {
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
