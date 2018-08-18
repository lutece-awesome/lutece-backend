<template>
	<v-container
		:class="{'pa-0': $vuetify.breakpoint.xsOnly }"
		fluid>
		<v-layout
			row
			wrap
			justify-center>
			<v-flex xs12>
				<Searchbar
					v-model = "filter"
					label = "Search user"
				/>
				<ApolloQuery
					:query = "require('@/graphql/user/list.gql')"
					:variables = "{ page , filter }"
					@result = "onResult">
					<template
						slot-scope = "{ result: { loading , error , data } }">
						<div v-if = "loading" >
							<LoadingSpinner />
						</div>
						<div v-else-if = "error" >An error occured</div>
						<div v-else-if = "data" >
							<UserList
								:user-item = "data.userList.userList"
							/>
							<div
								:class = "{'mb-2': $vuetify.breakpoint.xsOnly}"
								class = "text-xs-center">
								<v-pagination
									ref = "pagination"
									v-model = "page"
									:length = "maxpage"/>
							</div>
						</div>
					</template>
				</ApolloQuery>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
import UserList from '@/components/user/list/list';
import Searchbar from '@/components/basic/searchbar';
import LoadingSpinner from '@/components/basic/loadingspinner';


export default {
	name: 'User',
	metaInfo() { return { title: 'User' }; },
	components: {
		UserList,
		Searchbar,
		LoadingSpinner,
	},

	data() {
		return {
			page: 1,
			maxpage: 0,
			filter: '',
		};
	},

	activated() {
		if (this.$refs.pagination) { this.$refs.pagination.init(); }
	},


	methods: {
		onResult(result) {
			this.maxpage = result.data.userList.maxpage;
		},
	},

};
</script>
