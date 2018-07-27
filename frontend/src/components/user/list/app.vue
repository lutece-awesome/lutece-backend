<template>
	<v-layout
		row
		wrap
		justify-center>
		<v-flex xs12>
			<Searchbar
				v-model="filter"
				class="mb-3" />
			<UserList
				:user-item="userList"
				:is-loading="isLoading"/>
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
import UserList from '@/components/user/list/list';
import Searchbar from '@/components/basic/searchbar';
import UserListGQL from '@/graphql/user/list.gql';

const debounce = require('lodash.debounce');

export default {
	name: 'User',
	metaInfo() { return { title: 'User' }; },
	components: {
		UserList,
		Searchbar,
	},

	data() {
		return {
			isLoading: true,
			page: 1,
			maxpage: 0,
			userList: [],
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
		this.page = parseInt(localStorage.getItem('USER_LIST'), 10) || 1;
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
				query: UserListGQL,
				variables,
			})
				.then(response => response.data.userList)
				.then((data) => {
					Object.assign(this, data);
					this.page = Math.min(this.page, this.maxpage);
				})
				.then(() => { this.isLoading = false; });
			localStorage.setItem('USER_LIST', this.page);
		},
		debouncedRequest: debounce(function _debouncedRequest() {
			this.request();
		}, 250),
	},
};
</script>
