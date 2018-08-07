<template>
	<div>
		<v-textarea
			v-model = "content"
			auto-grow
			solo
		/>
		<!-- <v-card>
			<v-card-text>
				<div v-mixrend = "content" />
			</v-card-text>
		</v-card> -->
	</div>
</template>


<script>
export default {
	data: () => ({
		content: '',
	}),
};
</script>

<style>
    .v-textarea textarea {
        font-size: 14px !important;
        resize: none;
        font-family: 'Monaco', courier, monospace !important;
    }
</style>
