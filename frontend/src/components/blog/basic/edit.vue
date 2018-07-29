<template>
	<v-container>
		<v-layout
			row
			justify-center
			wrap>
			<v-flex
				xs12
				md8>
				<v-form
					@submit.prevent="submit"
				>
					<v-text-field
						v-model = "title_"
						:error-messages="geterror('title')"
						label="Title"
					/>
					<v-textarea
						v-model = "content_"
						:error-messages="geterror('content')"
						label="Content"
						auto-grow
					/>
					<v-btn
						:loading = "isloading"
						:color="error ? &quot;error&quot; : &quot;primary&quot;"
						block
						type = "submit"
					> Submit </v-btn>
				</v-form>
			</v-flex>
		</v-layout
	></v-container>
</template>

<script>
export default {
	props: {
		slug: {
			type: String,
			default: '',
		},
		title: {
			type: String,
			default: '',
		},
		content: {
			type: String,
			default: '',
		},
	},

	data: () => ({
		error: false,
		isloading: false,
		errordetail: {},
		title_: '',
		content_: '',
	}),

	mounted() {
		this.title_ = this.title;
		this.content_ = this.content;
	},

	methods: {
		geterror(field) {
			if (Object.prototype.hasOwnProperty.call(this.errordetail, field)) {
				return this.errordetail[field][0].message;
			}
			return '';
		},
		submit() {

		},
	},
};
</script>
