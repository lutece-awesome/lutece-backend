<template>
	<v-container align-center>
		<v-layout
			row
			wrap >
			<v-flex xs12>
				<div class = "text-xs-center" >
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
			type: Number,
			default: 200,
		},
		size: {
			type: Number,
			default: 30,
		},
	},
};
</script>
