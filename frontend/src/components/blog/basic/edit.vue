<template>
	<v-form>
		<v-text-field
			v-model = "value.title"
			:error-messages="geterror('title')"
			label="Title"
		/>
		<v-textarea
			v-model = "value.content"
			:error-messages="geterror('content')"
			label="Content"
			auto-grow
		/>
	</v-form>
</template>

<script>
export default {
	props: {
		value: {
			type: Object,
			default: null,
		},
		errordetail: {
			type: Object,
			default: () => ({}),
		},
	},

	methods: {
		geterror(field) {
			if (Object.prototype.hasOwnProperty.call(this.errordetail, field)) {
				return this.errordetail[field][0].message;
			}
			return '';
		},
	},
};
</script>
