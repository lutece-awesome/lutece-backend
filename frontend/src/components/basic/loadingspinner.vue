<template>
	<v-container align-center>
		<v-layout
			row
			wrap >
			<v-flex xs12>
				<div
					:style = "{ 'padding-top': height + 'px'}"
					class = "text-xs-center"
				>
					<v-progress-circular
						:size = "size"
						indeterminate
						color = "primary"
					/>
				</div>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
export default {
	props: {
		height: {
			type: String,
			default: '100',
		},
		size: {
			type: Number,
			default: 30,
		},
	},
};
</script>
