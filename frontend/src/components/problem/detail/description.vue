<template>
	<div
		class="ma-4">
		<div
			v-mixrend = "content"
			class="mb-3" />
		<h2
			v-if="standardInput"
			class="headline mb-3">Standard Input</h2>
		<div
			v-mixrend = "standardInput"
			class="mb-3" />
		<h2
			v-if="standardOutput"
			class="headline mb-3">Standard Output</h2>
		<div
			v-mixrend = "standardOutput"
			class="mb-3" />
		<h2
			v-if="constraints"
			class="headline mb-3">Constraints</h2>
		<div
			v-mixrend = "constraints"
			class="mb-3" />
		<h2 class="headline mb-3">Sample</h2>
		<table class="sample-table mb-3">
			<tr><th>Input</th><th>Output</th></tr>
			<tr
				v-for="(sample, index) in samples"
				:key="index">
				<td><pre>{{ sample.input }}</pre></td>
				<td><pre>{{ sample.output }}</pre></td>
			</tr>
		</table>
		<h2
			v-if="note"
			class="headline mb-3">Note</h2>
		<div class="mb-3">{{ note }}</div>
		<table class="guideline-table">
			<tr>
				<td>Time Limit</td>
				<td>{{ timeLimit }} ms</td>
			</tr>
			<tr>
				<td>Memory Limit</td>
				<td>{{ memoryLimit }} MiB</td>
			</tr>
			<tr v-if="resource">
				<td>Source</td>
				<td>{{ resource }}</td>
			</tr>
		</table>
	</div>
</template>

<script>
export default {
	props: {
		content: {
			type: String,
			required: false,
			default: '',
		},
		standardInput: {
			type: String,
			required: false,
			default: '',
		},
		standardOutput: {
			type: String,
			required: false,
			default: '',
		},
		constraints: {
			type: String,
			required: false,
			default: '',
		},
		resource: {
			type: String,
			required: false,
			default: '',
		},
		note: {
			type: String,
			required: false,
			default: '',
		},
		timeLimit: {
			type: Number,
			required: true,
		},
		memoryLimit: {
			type: Number,
			required: true,
		},
		samples: {
			type: Array,
			required: true,
		},
	},

	methods: {
		rend(_field) {

		},
	},
};
</script>
