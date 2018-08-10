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
				<Searchbar
					v-model="filter"
					label="Search problem by id, title or source" />
				<v-divider/>

				<ApolloQuery
					:query = "require('@/graphql/problem/list.gql')"
					:variables = "{ page , filter }"
					@result = "onResult" >
					<template
						slot-scope = "{ result: { loading , error , data } }">
						<div
							v-if = "loading"
						> Loading... </div>
						<div
							v-else-if = "error"
						>An error occured</div>
						<v-card>
							<ProblemList
								:problem-item = "data.problemList.problemList"
								:is-loading = "loading"/>
						</v-card>
					</template>
				</ApolloQuery>
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
import ProblemList from '@/components/problem/list/list';
import Searchbar from '@/components/basic/searchbar';

export default {
	name: 'Problem',
	metaInfo() { return { title: 'Problem' }; },
	components: {
		ProblemList,
		Searchbar,
	},

	data() {
		return {
			page: 1,
			maxpage: 0,
			filter: '',
		};
	},

	activated() {
		this.$refs.pagination.init();
	},

	methods: {
		onResult(result) {
			this.maxpage = result.data.problemList.maxpage;
		},
	},
};
</script>
