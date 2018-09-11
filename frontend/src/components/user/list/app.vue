<template>
	<v-container>
		<v-layout
			row
			wrap
			justify-center>
			<v-flex
				xs12
				md10
				lg8
			>
				<ApolloQuery
					:query = "require('@/graphql/user/list.gql')"
					:variables = "{ page , filter }"
					@result = "onResult">
					<template
						slot-scope = "{ result: { loading , error , data } }">
						<Searchbar
							v-model = "filter"
							class = "mb-4 fluid"
							label = ""
						/>
						<div v-if = "error" >An error occured</div>
						<div v-else-if = "data" >
							<v-hover>
								<v-card
									slot-scope = "{ hover }"
									:class = "`elevation-${hover ? 4 : 1}`"
								>
									<UserList
										:user-item = "data.userList.userList"
									/>
								</v-card>
							</v-hover>
							<div
								class = "text-xs-center mt-2">
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
