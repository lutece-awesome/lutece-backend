<template>
	<v-data-table
		:items = "userItem"
		:headers = "headers"
		:loading = "isLoading"
		hide-actions
	>
		<template
			slot="items"
			slot-scope="props">
			<td class = "text-xs-center">{{ getRank( props.item.rank ) }}</td>
			<td class = "text-xs-center" >
				<div style = "white-space: nowrap;">
					<v-avatar
						size = "32"
						color="grey lighten-4"
					>
						<img :src = "props.item.gravataremail" >
					</v-avatar>
					<router-link
						:to = "{ name: 'UserDetail' , params: {username: props.item.username } }"
						tag = "span"
						class = "body-2 ml-2"
						style = "cursor: pointer"
					>
						{{ props.item.displayName }}
					</router-link>
				</div>
			</td>
			<td class="text-xs-center">
				<span style = "color:green" > {{ props.item.solved }} </span>
				<span> / </span>
				<span style = "color:red" > {{ props.item.tried }} </span>
			</td>
			<td class = "text-xs-center">
				{{
					successRatio(
						props.item.submissionStatistics.accept ,
						props.item.submissionStatistics.reject )
				}} %
			</td>
		</template>
	</v-data-table>
</template>


<script>
export default {
	props: {
		userItem: {
			type: Array,
			default: () => [],
		},
		isLoading: {
			type: Boolean,
			default: false,
		},
	},
	data: () => ({
		hidden: false,
		headers: [
			{
				text: 'Rank',
				align: 'center',
				sortable: false,
			},
			{
				text: 'User',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Solved',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Ratio',
				align: 'center',
				sortable: false,
			},
		],
	}),
	methods: {
		successRatio(ac, rj) {
			if (ac + rj === 0) return '0.00';
			return ((ac / (ac + rj)) * 100.0).toFixed(2);
		},
		getRank(rk) {
			let s = String(rk);
			if (s.length < 2) s = `0${s}`;
			return s;
		},
	},
};
</script>
