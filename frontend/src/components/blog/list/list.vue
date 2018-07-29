<template>
	<v-data-table
		:items = "Item"
		:headers = "headers"
		:loading="isLoading"
		hide-actions
	>
		<template
			slot="items"
			slot-scope="props">
			<td class="text-xs-center">{{ props.item.id }}</td>
			<td class="text-xs-center">{{ props.item.title }}</td>
			<td class="text-xs-center">{{ props.item.vote }}</td>
			<td class="text-xs-center">{{ props.item.view }}</td>
		</template>
	</v-data-table>
</template>


<script>
export default {
	props: {
		Item: {
			type: Array,
			default: () => [],
		},
		isLoading: {
			type: Boolean,
			default: false,
		},
	},
	data: () => ({
		headers: [
			{
				text: '#',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Title',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Vote',
				align: 'center',
				sortable: false,
			},
			{
				text: 'View',
				align: 'center',
				sortable: false,
			},
		],
	}),
};
</script>
