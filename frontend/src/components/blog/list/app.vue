<template>
	<v-container
		:class="{'pa-0': $vuetify.breakpoint.xsOnly }"
		fluid>
		<v-layout
			row
			justify-center>
			<v-flex
				xs12
				md10
				lg8>
				<v-card>
					<BlogList
						:items = "items"
						:is-loading="isLoading"/>
				</v-card>
				<div
					:class="{'mb-2': $vuetify.breakpoint.xsOnly}"
					class="text-xs-center mt-2">
					<v-pagination
						ref="pagination"
						v-model="page"
						:length="maxpage"/>
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
import BLogListGQL from '@/graphql/blog/list.gql';
import BlogList from '@/components/blog/list/list';

export default {
	name: 'Blog',
	metaInfo() { return { title: 'Blog' }; },

	components: {
		BlogList,
	},

	data: () => ({
		isLoading: true,
		items: [],
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
		request() {
			const variables = {
				page: this.page,
			};
			this.isLoading = true;
			this.$apollo.query({
				query: BLogListGQL,
				variables,
			})
				.then(response => response.data.blogList)
				.then((data) => {
					this.items = data.blogList;
					this.maxpage = data.maxpage;
					this.page = Math.min(this.page, this.maxpage);
				})
				.then(() => { this.isLoading = false; });
		},
	},
};
</script>
