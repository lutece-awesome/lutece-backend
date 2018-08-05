<template>
	<div>
		<div
			v-for = "( discussion , index ) in value"
			:key = "index"
		>
			<comment :value = "discussion" />
			<comment
				v-for = "( reply , index) in discussion.reply"
				:key = "index"
				:value = "reply"
				is-reply
			/>
		</div>
	</div>
</template>

<script>
import comment from '@/components/comments/comment';

export default {
	components: {
		comment,
	},
	props: {
		value: {
			type: Array,
			default: () => ([]),
		},
	},
};
</script>
