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
						:item = "items"
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
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>
import BLogListGQL from '@/graphql/blog/list.gql';
import BlogList from '@/components/blog/list/list.vue';

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
				.then(response => response.data.problemList)
				.then((data) => {
					Object.assign(this, data);
					this.page = Math.min(this.page, this.maxpage);
				})
				.then(() => { this.isLoading = false; });
		},
	},
};
</script>
