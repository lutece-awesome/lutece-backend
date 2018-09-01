<template>
	<v-card>
		<v-card-text>
			<v-data-table
				:items = "judge"
				:headers = "headers"
				dense
				hide-actions>
				<template
					slot = "items"
					slot-scope = "props">
					<tr>
						<td class = "text-xs-center">{{ props.item.case }}</td>
						<td class = "text-xs-center">{{ props.item.result }}</td>
						<td class = "text-xs-center">{{ props.item.time_cost }} ms</td>
						<td class = "text-xs-center">{{ props.item.memory_cost }} KiB</td>
					</tr>
				</template>
			</v-data-table>
		</v-card-text>
	</v-card>
</template>

<script>
export default {
	props: {
		judge: {
			type: Array,
			default: () => ([]),
		},
		headers: {
			type: Array,
			default: null,
		},
	},
};
</script>
