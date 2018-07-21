<template>
	<v-autocomplete
		v-model = "model"
		:items = "items"
		:loading = "isLoading"
		:search-input.sync = "search"
		hide-details
		hide-no-data
		append-icon="mdi-magnify"
		return-object
		small-chips
		solo
		label="Search"/>
</template>

<script>
import ProblemSearchGQL from '@/graphql/problem/search.gql';

export default {
	data() {
		return {
			model: null,
			result: [],
			isLoading: false,
			search: null,
		};
	},

	computed: {
		items() {
			return this.result;
		},
	},

	watch: {
		search(val) {
			if (!val || val.length === 0 || this.isLoading) return;
			this.isLoading = true;
			this.$apollo.query({
				query: ProblemSearchGQL,
				variables: {
					title: val,
				},
			})
				.then(response => response.data.problemsearch)
				.then((data) => {
					this.result = data;
				})
				.finally(() => { this.isLoading = false; });
		},
	},
};
</script>
