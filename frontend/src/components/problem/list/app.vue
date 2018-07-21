<template>
	<v-layout
		row
		justify-center>
		<v-flex
			v-if = "!isLoading"
			xs12
			md8>
			<problemsearch class="mb-2" />
			<v-card>
				<ProblemList :problem-item="problemItem" />
			</v-card>
			<div class="text-xs-center mt-2">
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
			problemItem: [],
		};
	},

	watch: {
		page() {
			this.request(this.page);
		},
	},

	mounted() {
		const pre = localStorage.getItem('PROBLEM_LIST') || 1;
		this.page = pre;
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
					this.problemItem = data.problemList;
					this.maxpage = data.maxpage;
					this.page = Math.min(page, this.maxpage);
				})
				.then(() => { this.isLoading = false; });
			localStorage.setItem('PROBLEM_LIST', this.page);
		},
	},
};
</script>
