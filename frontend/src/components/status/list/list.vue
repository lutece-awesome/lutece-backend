<template>
	<v-data-table
		:items = "statusItem"
		:headers = "headers"
		hide-actions >
		<template
			slot="items"
			slot-scope = "props">
			<router-link
				:to="{name: &quot;ProblemDetailDescription&quot;, params: {slug: props.item.problem}}"
				:style="{cursor: 'pointer'}"
				tile
				tag="tr">
				<td class="text-xs-center">{{ props.item.submissionId }}</td>
				<td class="text-xs-center">{{ props.item.user }}</td>
				<td class="text-xs-center">{{ props.item.problem }}</td>
				<td class="text-xs-center">{{ props.item.judgeStatus.toUpperCase() }}</td>
				<td class="text-xs-center">{{ props.item.submitTime }}</td>
				<td class="text-xs-center">{{ props.item.language.toUpperCase() }}</td>
			</router-link>
		</template>
	</v-data-table>

</template>


<script>
export default {
	props: {
		statusItem: {
			type: Array,
			default: () => [],
		},
	},
	data: () => ({
		hidden: false,
		headers: [
			{
				text: '#',
				align: 'center',
				sortable: false,
			},
			{
				text: 'User',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Title',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Verdict',
				align: 'center',
				sortable: false,
				class: 'hidden-sm-and-down',
			},
			{
				text: 'When',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Language',
				align: 'center',
				sortable: false,
			},
		],
	}),
};
</script>
