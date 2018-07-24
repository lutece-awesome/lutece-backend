<template>
	<v-data-table
		:items = "statusItem"
		:headers = "headers"
		hide-actions >
		<template
			slot="items"
			slot-scope="props">
			<router-link
				:to="{name: &quot;StatusDetail&quot;, params: {pk: props.item.submissionId}}"
				:style="{cursor: 'pointer'}"
				tile
				tag="tr">
				<td class="text-xs-center">{{ props.item.submissionId }}</td>
				<td class="text-xs-center">{{ props.item.user }}</td>
				<td class="text-xs-center">{{ props.item.problem }}</td>
				<td
					:class="props.item.color + '--text'"
					class="text-xs-center">
					{{ props.item.judgeStatus }}
					<span v-if="props.item.failedCase">#{{ props.item.failedCase }}</span>
				</td>
				<td class="text-xs-center">{{ props.item.timecost }}</td>
				<td class="text-xs-center">{{ props.item.memorycost }}</td>
				<td class="text-xs-center time">
					<span class="humanize-time">{{ props.item.submitTime | moment("from") }}</span>
					<span class="full-time">{{ props.item.submitTime | moment("Y-MM-DD HH:mm:ss") }}</span>
				</td>
				<td class="text-xs-center">{{ props.item.language }}</td>
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
				text: 'Problem',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Verdict',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Time (ms)',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Memory (KiB)',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Submit Time',
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
