<template>
	<v-card-text>
		<CodeEditor/>
	</v-card-text>
</template>

<script>

export default {
	components: {
		CodeEditor: () => import('@/components/basic/codeeditor'),
	},
};
</script>
