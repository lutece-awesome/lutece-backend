<template>
	<v-container
		v-if="problem"
		fiuld>
		<div
			v-mixrend = "problem.content"
			class="mb-3" />
		<h2
			v-if="problem.standardInput"
			class="headline mb-3">Standard Input</h2>
		<div
			v-mixrend = "problem.standardInput"
			class="mb-3" />
		<h2
			v-if="problem.standardOutput"
			class="headline mb-3">Standard Output</h2>
		<div
			v-mixrend = "problem.standardOutput"
			class="mb-3" />
		<h2
			v-if="problem.constraints"
			class="headline mb-3">Constraints</h2>
		<div
			v-mixrend = "problem.constraints"
			class="mb-3" />
		<h2 class="headline mb-3">Sample</h2>
		<table class="sample-table mb-3">
			<tr><th>Input</th><th>Output</th></tr>
			<tr
				v-for="(sample, index) in problem.sampleSet"
				:key="index">
				<td><pre>{{ sample.inputContent }}</pre></td>
				<td><pre>{{ sample.outputContent }}</pre></td>
			</tr>
		</table>
		<h2
			v-if="problem.note"
			class="headline mb-3">Note</h2>
		<div class="mb-3">{{ problem.note }}</div>
		<table class="guideline-table">
			<tr>
				<td>Problem ID</td>
				<td>{{ problem.problemId }}</td>
			</tr>
			<tr>
				<td>Time Limit</td>
				<td>{{ problem.timeLimit }} ms</td>
			</tr>
			<tr>
				<td>Memory Limit</td>
				<td>{{ problem.memoryLimit }} MiB</td>
			</tr>
			<tr v-if="problem.resource">
				<td>Source</td>
				<td>{{ problem.resource }}</td>
			</tr>
		</table>
	</v-container>
</template>

<script>
export default {
	props: {
		problem: {
			type: Object,
			default: null,
		},
	},

	methods: {
		rend(_field) {

		},
	},
};
</script>
