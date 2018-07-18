<template>
	<v-layout
		row
		wrap
		justify-center>
		<v-flex
			xs12
			md10
			xl8>
			<v-card>
				<v-toolbar
					card
					prominent
					tabs>
					<v-toolbar-title>
						{{ title }}
					</v-toolbar-title>
					<v-tabs
						slot="extension"
						v-model="tabs"
						fixed-tabs
						color="transparent"
						@input="tabChanged">
						<v-tab
							:ripple="false"
							to="description">Description</v-tab>
						<v-tab
							:ripple="false"
							to="editor">Editor</v-tab>
						<v-tab
							:ripple="false"
							to="discussion">Discussion</v-tab>
					</v-tabs>
				</v-toolbar>
				<v-tabs-items
					v-model="tabs"
					touchless>
					<v-tab-item id="description">
						<ProblemDescription
							:content = "content"
							:standard-input = "standardInput"
							:standard-output = "standardOutput"
							:constraints = "constraints" />
					</v-tab-item>
					<v-tab-item id="editor">
						<ProblemEditor ref="problemEditor"/>
					</v-tab-item>
					<v-tab-item id="discussion">
						<ProblemDiscussion/>
					</v-tab-item>
				</v-tabs-items>
			</v-card>
		</v-flex>
	</v-layout>
</template>

<script>
import ProblemDescription from '@/components/problem/detail/description';
import ProblemEditor from '@/components/problem/detail/editor';
import ProblemDiscussion from '@/components/problem/detail/discussion';
import ProblemDetailGQL from '@/graphql/problem/detail.gql';

export default {
	metaInfo() { return { title: this.title || 'Loading...' }; },
	components: {
		ProblemDescription,
		ProblemEditor,
		ProblemDiscussion,
	},
	data: () => ({
		slug: '',
		isLoading: false,
		tabs: null,
		title: '',
		content: '',
		standardInput: '',
		standardOutput: '',
		constraints: '',
		resource: '',
		note: '',
		timeLimit: 0,
		memoryLimit: 0,
	}),

	mounted() {
		this.slug = this.$route.params.slug;
		this.request();
	},
	methods: {
		request() {
			this.$apollo.query({
				query: ProblemDetailGQL,
				variables: {
					slug: this.slug,
				},
			})
				.then(response => response.data.problem)
				.then((data) => {
					this.title = data.title;
					this.content = data.content;
					this.standardInput = data.standardInput;
					this.standardOutput = data.standardOutput;
					this.constraints = data.constraints;
					this.resource = data.resource;
					this.note = data.note;
					this.timeLimit = data.timeLimit;
					this.memoryLimit = data.memoryLimit;
				});
		},
		tabChanged() {
			if (this.$refs.problemEditor
				&& this.$refs.problemEditor.$refs.codeMirror
				&& this.$refs.problemEditor.$refs.codeMirror.$refs.codeMirror) {
				const cm = this.$refs.problemEditor.$refs.codeMirror.$refs.codeMirror;
				cm.refresh();
			}
		},
	},
};
</script>
