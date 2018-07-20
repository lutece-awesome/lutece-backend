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
						Status
					</v-toolbar-title>
					<v-spacer/>
				</v-toolbar>
				<StatusList :status-item = "statusItem" />
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

import StatusList from '@/components/status/list/list';
import StatusListGQL from '@/graphql/submission/list.gql';


export default {

	components: {
		StatusList,
	},

	data() {
		return {
			isLoading: false,
			page: 0,
			maxpage: 0,
			statusItem: [],
		};
	},

	watch: {
		page() {
			this.request(this.page);
		},
	},

	mounted() {
		const pre = localStorage.getItem('STATUS_LIST') || 1;
		this.page = pre;
	},

	methods: {
		request(page) {
			this.isLoading = true;
			page = parseInt(page, 10);
			this.$apollo.query({
				query: StatusListGQL,
				variables: {
					page,
				},
			})
				.then(response => response.data.submissionList)
				.then((data) => {
					this.statusItem = data.submissionList;
					this.maxpage = data.maxpage;
					this.page = Math.min(page, this.maxpage);
				})
				.then(() => { this.isLoading = false; });
			localStorage.setItem('STATUS_LIST', this.page);
		},
	},
};
</script>
