<template>
	<v-card hover>
		<v-text-field
			:value = "value"
			:label = "label"
			hide-details
			append-icon = "mdi-magnify"
			solo
			flat
			type = "search"
			@input = "$emit('input', $event)"/>
	</v-card>
</template>

<script>

export default {
	props: {
		value: {
			type: String,
			required: true,
		},
		label: {
			type: String,
			default: 'Search',
		},
	},
};
</script>
