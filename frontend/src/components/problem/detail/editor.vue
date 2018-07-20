<template>
	<CodeEditor :problemslug = "problemslug" />
</template>

<script>

export default {
	components: {
		CodeEditor: () => import('@/components/basic/codeeditor'),
	},
	props: {
		problemslug: {
			type: String,
			required: true,
		},
	},
};
</script>
