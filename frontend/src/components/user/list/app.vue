<template>
	<v-layout
		row
		justify-center>
		<v-flex xs12>
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
import UserListGQL from '@/graphql/user/list.gql';

export default {
	metaInfo() { return { title: 'User' }; },
	components: {
		UserList,
	},

	data() {
		return {
			isLoading: true,
			page: 0,
			maxpage: 0,
			userList: [],
		};
	},

	watch: {
		page() {
			this.request(this.page);
		},
	},

	mounted() {
		this.page = parseInt(localStorage.getItem('USER_LIST'), 10) || 1;
	},

	methods: {
		request(page) {
			this.isLoading = true;
			this.$apollo.query({
				query: UserListGQL,
				variables: {
					page,
				},
			})
				.then(response => response.data.userList)
				.then((data) => {
					Object.assign(this, data);
					this.page = Math.min(this.page, this.maxpage);
				})
				.then(() => { this.isLoading = false; });
			localStorage.setItem('USER_LIST', this.page);
		},
	},
};
</script>
