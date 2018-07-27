<template>

	<v-layout
		row
		justify-center>
		<v-flex
			xs12
			xl10>
			<v-card>
				<StatusList
					:status-item="submissionList"
					:filter="filter"
					:is-loading="isLoading" />
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

import StatusList from '@/components/status/list/list';
import StatusListGQL from '@/graphql/submission/list.gql';

const debounce = require('lodash.debounce');

export default {
	metaInfo() { return { title: 'Status' }; },

	components: {
		StatusList,
	},

	data() {
		return {
			isLoading: false,
			page: 0,
			maxpage: 0,
			submissionList: [],
			filter: {
			},
		};
	},

	watch: {
		page() {
			this.request();
		},
		filter: {
			handler() {
				this.isLoading = true;
				debounce(this.request, 250, { maxWait: 1000 })();
			},
			deep: true,
		},
	},

	mounted() {
		if (this.page === 0) { this.page = 1; }
	},

	methods: {
		request() {
			const filter = {};
			if (this.filter.pk) {
				filter.pk = parseInt(this.filter.pk, 10);
			}
			filter.user = this.filter.user;
			filter.problem = this.filter.problem;
			filter.judgeStatus = this.filter.judgeStatus;
			filter.language = this.filter.language;
			this.isLoading = true;
			this.$apollo.query({
				query: StatusListGQL,
				variables: {
					page: this.page,
					date: new Date().getTime(),
					...filter,
				},
			})
				.then(response => response.data.submissionList)
				.then((data) => {
					Object.assign(this, data);
					this.page = Math.min(this.page, this.maxpage);
				})
				.then(() => { this.isLoading = false; });
		},
	},
};
</script>
