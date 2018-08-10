<template>
	<div>
		<!-- <v-data-table
			:items = "items"
			:headers = "headers"
			:loading="isLoading"
			hide-actions
		>
			<template
				slot="items"
				slot-scope="props">
				<router-link
					:to="{name: 'BlogDetail', params: {slug: props.item.slug }}"
					:style="{cursor: 'pointer'}"
					tile
					tag="tr">
					<td class="text-xs-center">{{ props.item.id }}</td>
					<td class="text-xs-center">{{ props.item.title }}</td>
					<td class="text-xs-center">{{ props.item.vote }}</td>
					<td class="text-xs-center">{{ props.item.view }}</td>
				</router-link>
			</template>
		</v-data-table> -->
	</div>
</template>


<script>
export default {
	props: {
		items: {
			type: Array,
			default: () => [],
		},
		isLoading: {
			type: Boolean,
			default: false,
		},
	},
};
</script>
