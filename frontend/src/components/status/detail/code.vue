<template>
	<v-card>
		<v-card-text>
			<codemirror
				v-if = "code"
				v-model = "code"
				:options = "cmOptions"
			/>
			<div
				v-if="judgererror_msg"
				class="output-code">
				<pre>{{ judgererror_msg }}</pre>
			</div>
			<div
				v-if="compileerror_msg"
				class="output-code">
				<pre>{{ compileerror_msg }}</pre>
			</div>
		</v-card-text>
	</v-card>
</template>


<script>
export default {
	components: {
		codemirror: () => import('@/components/basic/codemirror'),
	},
	props: {
		code: {
			type: String,
			default: null,
		},
		judgererror_msg: {
			type: String,
			default: null,
		},
		compileerror_msg: {
			type: String,
			default: null,
		},
		cmOptions: {
			type: Object,
			default: null,
		},
	},
};
</script>
