<template>
	<div v-show = "display" >
		<v-toolbar
			dense
			height = "40">
			<v-btn
				flat
				small
				@click = "previewContent">
				<v-icon
					v-show = "!preview"
					small> mdi-eye </v-icon>
				<v-icon
					v-show = "preview"
					small> mdi-eye-off </v-icon>
				<span class = "ml-2" > PREVIEW </span>
			</v-btn>
			<v-btn
				small
				flat>
				<v-icon small>mdi-image</v-icon>
				<span class = "ml-2" > UPLOAD </span>
			</v-btn>
			<v-spacer/>
			<a @click = "$emit('close-editor')" >
				<v-icon> mdi-close-circle </v-icon>
			</a>
		</v-toolbar>
		<v-textarea
			v-show = "!preview"
			v-model = "content"
			class = "commentEditor"
			auto-grow
			solo
		/>
		<v-card v-if = "preview">
			<v-card-text>
				<div>
					<div
						v-mixrend = "content"
						class = "commentContent" />
				</div>
			</v-card-text>
		</v-card>
	</div>
</template>


<script>
export default {

	props: {
		display: {
			type: Boolean,
			required: true,
			default: false,
		},
	},
	data: () => ({
		content: '',
		preview: false,
	}),

	methods: {
		previewContent() {
			this.preview = !this.preview;
		},
	},
};
</script>

<style>
    .v-textarea.commentEditor textarea {
        font-size: 14px !important;
        resize: none;
        font-family: 'Monaco', courier, monospace !important;
		line-height: 1.5rem;
    }
</style>
