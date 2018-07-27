<template>
	<v-text-field
		:value="value"
		:label="label"
		hide-details
		append-icon="mdi-magnify"
		solo
		type="search"
		@input="$emit('input', $event)"/>
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
