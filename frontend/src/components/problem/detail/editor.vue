<template>
	<CodeEditor :problemslug = "problemslug" />
</template>

<script>

import CodeEditor from '@/components/basic/codeeditor';

export default {
	components: {
		CodeEditor,
	},
	props: {
		problemslug: {
			type: String,
			required: true,
		},
	},
};
</script>
