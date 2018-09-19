<template>
	<v-layout
		slot="placeholder"
		fill-height
		align-center
		justify-center
		ma-0
	>
		<v-progress-circular
			:size = "size"
			indeterminate
			color = "primary"
		/>
	</v-layout>
</template>

<script>
export default {
	props: {
		size: {
			type: Number,
			default: 30,
		},
	},
};
</script>
