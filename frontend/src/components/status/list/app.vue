<template>
	<v-container
		:class="{'pa-0': $vuetify.breakpoint.xsOnly }"
		fluid>
		<v-layout
			row
			justify-center>
			<v-flex
				xs12
				xl10>
				<v-card>
					<StatusList
						:status-item="submissionList"
						:filters="filters"
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
	</v-container>
</template>


<script>

import StatusList from '@/components/status/list/list';
import StatusListGQL from '@/graphql/submission/list.gql';

const debounce = require('lodash.debounce');


export default {
	name: 'Status',
	metaInfo() { return { title: 'Status' }; },

	components: {
		StatusList,
	},

	data() {
		return {
			isLoading: false,
			page: 1,
			maxpage: 0,
			submissionList: [],
			filters: { },
		};
	},

	watch: {
		page() {
			this.request();
		},
		filters: {
			handler() {
				this.isLoading = true;
				this.debouncedRequest();
			},
			deep: true,
		},
	},

	mounted() {
		this.request();
	},

	methods: {
		request() {
			const variables = {
				page: this.page,
				date: new Date().getTime(),
				...this.filters,
			};
			variables.pk = parseInt(variables.pk, 10);
			this.isLoading = true;
			this.$apollo.query({
				query: StatusListGQL,
				variables,
			})
				.then(response => response.data.submissionList)
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
