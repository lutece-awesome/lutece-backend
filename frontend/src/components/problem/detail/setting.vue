<template>
	<v-container
		v-if="value"
		fiuld>
		<v-form>
			<v-text-field
				v-model="value.title"
				label="Title"
			/>
			<v-textarea
				v-model="value.content"
				label="Content"
				auto-grow
				rows="1"
			/>
			<v-textarea
				v-model="value.standardInput"
				label="Standard Input"
				auto-grow
				rows="1"
			/>
			<v-textarea
				v-model="value.standardOutput"
				label="Standard Output"
				auto-grow
				rows="1"
			/>
			<v-textarea
				v-model="value.constraints"
				label="Constraints"
				auto-grow
				rows="1"
			/>
			<v-text-field
				v-model="value.resource"
				label="resource"
			/>
			<div
				v-for = "(each , index) in value.sampleSet"
				:key = "index">
				<span>
					{{ each.inputContent }}
				</span>
				<span>
					{{ each.outputContent }}
				</span>
			</div>
			<v-btn> ADD SAMPLE </v-btn>
			<v-textarea
				v-model="value.note"
				label="Note"
				auto-grow
				rows="1"
			/>
			<v-text-field
				v-model="value.timeLimit"
				type= "number"
				label="TimeLimit"
			/>
			<v-text-field
				v-model="value.memoryLimit"
				type= "number"
				label="MemoryLimit"
			/>
			<v-btn> SUBMIT </v-btn>
		</v-form>
	</v-container>
</template>


<script>
export default {
	props: {
		value: {
			type: Object,
			default: null,
		},
	},

	methods: {

		submit() {

		},

	},
};
</script>
