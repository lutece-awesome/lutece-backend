<template>
	<CodeEditor ref="codeMirror"/>
</template>

<script>

export default {
	components: {
		CodeEditor: () => import('@/components/basic/codeeditor'),
	},
};
</script>
