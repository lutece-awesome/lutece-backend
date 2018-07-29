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
					<Searchbar
						v-model="filter"
						label="E.g. &quot;A+B&quot;, &quot;#123&quot;, &quot;#1230-1235&quot;" />
					<v-divider/>
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
	</v-container>
</template>

<script>
import ProblemList from '@/components/problem/list/list';
import Searchbar from '@/components/basic/searchbar';
import ProblemListGQL from '@/graphql/problem/list.gql';

const debounce = require('lodash.debounce');

export default {
	name: 'Problem',
	metaInfo() { return { title: 'Problem' }; },
	components: {
		ProblemList,
		Searchbar,
	},

	data() {
		return {
			isLoading: true,
			page: 1,
			maxpage: 0,
			problemList: [],
			filter: '',
		};
	},

	watch: {
		page() {
			this.request();
		},
		filter() {
			this.isLoading = true;
			this.debouncedRequest();
		},
	},

	mounted() {
		this.request();
	},

	methods: {
		request() {
			const variables = {
				page: this.page,
				filter: this.filter,
			};
			this.isLoading = true;
			this.$apollo.query({
				query: ProblemListGQL,
				variables,
			})
				.then(response => response.data.problemList)
				.then((data) => {
					Object.assign(this, data);
					this.page = Math.min(this.page, this.maxpage);
				})
				.then(() => { this.isLoading = false; });
		},
		debouncedRequest: debounce(function _debouncedRequest() {
			this.request();
		}, 250),
	},
};
</script>
