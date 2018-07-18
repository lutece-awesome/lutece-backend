<template>
	<v-layout
		row
		justify-center>
		<v-flex
			v-if = "!isLoading"
			xs12
			md8>
			<v-card>
				<v-toolbar
					card
					prominent>
					<v-toolbar-title>
						Problem
					</v-toolbar-title>
					<v-spacer/>
					<problemsearch />
				</v-toolbar>
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
import ProblemList from '@/components/problem/list';
import Loading from '@/components/basic/loading';
import problemsearch from '@/components/basic/problemsearch';
import ProblemListGQL from '@/graphql/problem/list.gql';

export default {
	metaInfo() { return { title: 'Problem' }; },
	components: {
		ProblemList,
		Loading,
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
		this.request(pre);
	},

	methods: {
		request(page) {
			this.isLoading = true;
			this.page = parseInt(page, 10);
			this.$apollo.query({
				query: ProblemListGQL,
				variables: {
					page: this.page,
				},
			})
				.then(response => response.data.problemList)
				.then((data) => {
					this.problemItem = data.problemList;
					this.maxpage = data.maxpage;
					this.page = Math.min(this.page, this.maxpage);
				})
				.then(() => { this.isLoading = false; });
			localStorage.setItem('PROBLEM_LIST', this.page);
		},
	},
};
</script>
