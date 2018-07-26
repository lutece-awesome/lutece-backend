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
		};
	},

	watch: {
		page() {
			this.request(this.page);
		},
	},

	mounted() {
		if (this.page === 0) { this.page = 1; }
	},

	methods: {
		request(page) {
			this.isLoading = true;
			this.$apollo.query({
				query: StatusListGQL,
				variables: {
					page,
					date: new Date().getTime(),
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
