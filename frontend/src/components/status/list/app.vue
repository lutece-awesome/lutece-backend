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
						:user-search="userSearch"
						:problem-search="problemSearch"
						:is-loading="isLoading" />
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

import StatusList from '@/components/status/list/list';
import StatusListGQL from '@/graphql/submission/list.gql';
import UserSearchGQL from '@/graphql/user/search.gql';
import ProblemSearchGQL from '@/graphql/problem/search.gql';
import { mapGetters } from 'vuex';

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
			userSearch: {
				items: [],
				isLoading: false,
				filter: '',
			},
			problemSearch: {
				items: [],
				isLoading: false,
				filter: '',
			},
		};
	},
	computed: {
		userSearchFilter() {
			return this.userSearch.filter;
		},
		problemSearchFilter() {
			return this.problemSearch.filter;
		},
		...mapGetters({
			profile: 'user/profile',
			isAuthenticated: 'user/isAuthenticated',
		}),
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
		userSearchFilter() {
			this.updateUserSearch();
		},
		problemSearchFilter() {
			this.updateProblemSearch();
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
				.then(() => {
					this.isLoading = false;
				});
		},
		debouncedRequest: debounce(function _debouncedRequest() {
			this.request();
		}, 250),
		updateUserSearch() {
			if (!this.userSearchFilter) {
				if (this.isAuthenticated) {
					this.userSearch.items = [this.profile.displayName];
				} else {
					this.userSearch.items = [];
				}
				return;
			}
			const variables = {
				filter: this.userSearchFilter,
			};
			this.userSearch.isLoading = true;
			this.$apollo.query({
				query: UserSearchGQL,
				variables,
			})
				.then(response => response.data.userSearch)
				.then((data) => {
					this.userSearch.items = data.userList.map(val => val.displayName);
				})
				.then(() => { this.userSearch.isLoading = false; });
		},
		updateProblemSearch() {
			if (!this.problemSearchFilter) {
				this.problemSearch.items = [];
				return;
			}
			const variables = {
				filter: this.problemSearchFilter,
			};
			this.problemSearch.isLoading = true;
			this.$apollo.query({
				query: ProblemSearchGQL,
				variables,
			})
				.then(response => response.data.problemSearch)
				.then((data) => {
					this.problemSearch.items = data.problemList.map(val => val.title);
				})
				.then(() => { this.problemSearch.isLoading = false; });
		},
	},
};
</script>
