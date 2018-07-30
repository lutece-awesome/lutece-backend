<template>
	<v-container>
		<v-layout
			row
			justify-center
			wrap>
			<v-flex
				xs12
				md6>
				<BlogEdit
					:value = "value"
				/>
				<v-btn
					:loading = "isloading"
					:color="error ? &quot;error&quot; : &quot;primary&quot;"
					block
					@click = "submit"
				> Submit </v-btn>
			</v-flex>
			<v-flex
				xs12
				md6>
				<div
					v-mixrend = "value.content"
					class="mb-3" />
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>

import BlogEdit from '@/components/blog/basic/edit';

export default {
	components: {
		BlogEdit,
	},
	data: () => ({
		value: {
			title: '',
			content: '',
		},
		isloading: false,
		error: false,
	}),

	methods: {
		submit() {
			alert(this.value.title);
			alert(this.value.content);
		},
	},

};
</script>
