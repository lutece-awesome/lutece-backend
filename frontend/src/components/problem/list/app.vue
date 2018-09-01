<template>
	<v-container
		fluid>
		<v-layout
			row
			wrap
			justify-center>
			<v-flex xs12>
				<Searchbar
					v-model = "filter"
					class = "mb-4 fluid"
					label = "Search problem" />
			</v-flex>
			<v-flex
				xs12
				md10
				lg8>
				<ApolloQuery
					:query = "require('@/graphql/problem/list.gql')"
					:variables = "{ page , filter }"
					@result = "onResult" >
					<template
						slot-scope = "{ result: { loading , error , data } }">
						<div v-if = "loading" > <LoadingSpinner/> </div>
						<div v-else-if = "error"> An error occured</div>
						<div v-else-if = "data">
							<v-card
								hover
								style = "cursor: default"
							>
								<ProblemList
									:problem-item = "data.problemList.problemList"
									:is-loading = "loading"
								/>
							</v-card>
							<div
								:class="{'mb-2': $vuetify.breakpoint.xsOnly}"
								class="text-xs-center mt-2">
								<v-pagination
									ref="pagination"
									v-model="page"
									:length="maxpage"/>
							</div>
						</div>
					</template>
				</ApolloQuery>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
import ProblemList from '@/components/problem/list/list';
import Searchbar from '@/components/basic/searchbar';
import LoadingSpinner from '@/components/basic/loadingspinner';

export default {
	name: 'Problem',
	metaInfo() { return { title: 'Problem' }; },
	components: {
		ProblemList,
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
			this.maxpage = result.data.problemList.maxpage;
		},
	},
};
</script>
