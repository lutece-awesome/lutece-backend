<template>
	<v-hover>
		<v-card
			slot-scope = "{ hover }"
			:class = "`elevation-${hover || isFocus ? 4 : 1}`"
		>
			<v-text-field
				:value = "value"
				:label = "label"
				hide-details
				prepend-inner-icon = "mdi-magnify"
				solo
				flat
				type = "search"
				@focus = "setFocus"
				@blur = "removeFocus"
				@input = "$emit('input', $event)"/>
		</v-card>
	</v-hover>
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
	data: () => ({
		isFocus: false,
	}),
	methods: {
		setFocus() {
			this.isFocus = true;
		},
		removeFocus() {
			this.isFocus = false;
		},
	},
};
</script>
