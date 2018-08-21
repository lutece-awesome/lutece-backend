<template>
	<v-container align-center>
		<v-layout
			row
			wrap >
			<v-flex xs12>
				<Circle8
					:size = "String(size) + 'px'"
					:style = "{ margin : height / 2 + 'px auto' }"
				/>
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>
import { Circle8 } from 'vue-loading-spinner';

export default {
	components: {
		Circle8,
	},
	props: {
		height: {
			type: Number,
			default: 200,
		},
		size: {
			type: Number,
			default: 55,
		},
	},
};
</script>

<style scoped>

</style>
