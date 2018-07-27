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
				<v-tabs
					v-if="title"
					v-model="tabs"
					fixed-tabs>
					<v-tab
						:ripple="false"
						to="description">Description</v-tab>
					<v-tab
						:ripple="false"
						to="editor">Editor</v-tab>
					<v-tab
						:ripple="false"
						to="discussion">Disscussion</v-tab>
					<v-tab
						v-if="has_permission('problem.change_problem')"
						:ripple="false"
						to="edit">Edit</v-tab>
				</v-tabs>
				<v-tabs-items
					v-if="title"
					v-model="tabs"
					touchless>
					<v-tab-item id="description">
						<ProblemDescription
							:problem-id = "problemId"
							:content = "content"
							:standard-input = "standardInput"
							:standard-output = "standardOutput"
							:constraints = "constraints"
							:note = "note"
							:time-limit = "timeLimit"
							:memory-limit = "memoryLimit"
							:samples = "samples"
							:resource = "resource"
						/>
					</v-tab-item>
					<v-tab-item id="editor">
						<ProblemEditor :problemslug = "slug" />
					</v-tab-item>
					<v-tab-item id="discussion">
						<ProblemDiscussion/>
					</v-tab-item>
					<v-tab-item id="edit">
						<ProblemEdit
							:title = "title"
							:visible = "visible"
							:discussionvisible = "discussionvisible"
							:content = "content"
							:standard-input = "standardInput"
							:standard-output = "standardOutput"
							:constraints = "constraints"
							:note = "note"
							:time-limit = "timeLimit"
							:memory-limit = "memoryLimit"
							:samples = "samples"
							:resource = "resource"
							:slug = "slug"
						/>
					</v-tab-item>
				</v-tabs-items>
			</v-card>
		</v-flex>
	</v-layout>
</template>

<script>
import ProblemDescription from '@/components/problem/detail/description';
import ProblemEditor from '@/components/problem/detail/editor';
import ProblemSubmission from '@/components/problem/detail/submission';
import ProblemDiscussion from '@/components/problem/detail/discussion';
import ProblemEdit from '@/components/problem/detail/edit';
import ProblemDetailGQL from '@/graphql/problem/detail.gql';

export default {
	metaInfo() { return { title: this.title || 'Loading...' }; },
	components: {
		ProblemDescription,
		ProblemEditor,
		ProblemDiscussion,
		ProblemSubmission,
		ProblemEdit,
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
		problemId: null,
		timeLimit: null,
		memoryLimit: null,
		visible: null,
		discussionvisible: null,
		samples: [],
		has_permission: null,
	}),

	mounted() {
		this.slug = this.$route.params.slug;
		this.has_permission = this.$store.getters['user/has_permission'];
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
					Object.assign(this, data);
					this.samples = JSON.parse(this.sample);
				});
		},
	},
};
</script>
