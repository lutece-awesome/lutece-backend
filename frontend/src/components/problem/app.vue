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
						Problem
					</v-toolbar-title>
					<v-spacer/>
					<problemsearch />
				</v-toolbar>
				<ProblemList :problem-item="problemItem" />
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
import ProblemList from '@/components/problem/list.vue'
import Loading from '@/components/basic/loading.vue'
import problemsearch from '@/components/basic/problemsearch.vue'
import {
	ProblemListGQL
} from '@/graphql/problem/list.js'
export default {

	components: {
		ProblemList,
		Loading,
		problemsearch
	},

	data: function () {
		return {
			isLoading: true,
			page: 0,
			maxpage: 0,
			problemItem: []
		}
	},

	watch: {
		page: function () {
			this.request(this.page)
		}
	},

	mounted () {
		const pre = localStorage.getItem('PROBLEM_LIST') || 1
		this.request(pre)
	},

	methods: {
		request: function (page) {
			this.isLoading = true
			this.page = parseInt(page)
			this.$apollo.query({
				query: ProblemListGQL,
				variables: {
					page: this.page
				}
			})
				.then(response => response.data.problemList)
				.then(data => {
					this.problemItem = data.problemList
					this.maxpage = data.maxpage
					this.page = Math.min(this.page, this.maxpage)
				})
				.then(() => { this.isLoading = false })
			localStorage.setItem('PROBLEM_LIST', this.page)
		}
	}
}
</script>
