<template>
	<v-layout
		row
		justify-center>
		<v-flex
			xs12
			md10
			lg8>
			<!-- <problemsearch class="mb-2" /> -->
			<v-card>
				<ProblemList
					:problem-item="problemList"
					:is-loading="isLoading"/>
			</v-card>
			<div
				:class="{'mb-2': $vuetify.breakpoint.xsOnly}"
				class="text-xs-center mt-2">
				<v-pagination
					v-model="page"
					:length="maxpage"/>
			</div>
		</v-flex>
	</v-layout>
</template>

<script>
import ProblemList from '@/components/problem/list/list';
import problemsearch from '@/components/basic/problemsearch';
import ProblemListGQL from '@/graphql/problem/list.gql';

export default {
	metaInfo() { return { title: 'Problem' }; },
	components: {
		ProblemList,
		problemsearch,
	},

	data() {
		return {
			isLoading: true,
			page: 0,
			maxpage: 0,
			problemList: [],
		};
	},

	watch: {
		page() {
			this.request(this.page);
		},
	},

	mounted() {
		this.page = 1;
	},

	methods: {
		request(page) {
			this.isLoading = true;
			this.$apollo.query({
				query: ProblemListGQL,
				variables: {
					page,
				},
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
