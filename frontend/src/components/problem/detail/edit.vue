<template>
	<v-container
		:class="{'pa-0': $vuetify.breakpoint.xsOnly }"
		fluid
		grid-list-lg
		class="ma-0">
		<v-layout
			row
			wrap>
			<v-flex
				xs12
				md6>
				<v-card>
					<v-card-title primary-title>
						<h3 class="headline">Edit</h3>
					</v-card-title>
					<ProblemSetting v-model="problem"/>
				</v-card>
			</v-flex>
			<v-flex
				xs12
				md6>
				<v-card>
					<v-card-title primary-title>
						<h3 class="headline">Preview</h3>
					</v-card-title>
					<ProblemDescription :problem = "problem" />
				</v-card>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
import ProblemDescription from '@/components/problem/detail/description';
import ProblemSetting from '@/components/problem/detail/setting';
import ProblemDetailGQL from '@/graphql/problem/detail.gql';
import UpdateProblem from '@/graphql/problem/edit.gql';

export default {
	metaInfo() { return { title: this.problem ? `Edit ${this.problem.title}` : 'Loading...' }; },
	components: {
		ProblemDescription,
		ProblemSetting,
	},
	data: () => ({
		slug: '',
		problem: null,
	}),

	mounted() {
		this.slug = this.$route.params.slug;
		this.request();
	},

	methods: {
		submit() {
			this.$apollo.mutate({
				mutation: UpdateProblem,
				variables: {
					title: this.title,
					content: this.content,
					note: this.note,
					timeLimit: this.timeLimit,
					memoryLimit: this.memoryLimit,
					constraints: this.constraints,
					resource: this.resource,
					standardInput: this.standardInput,
					standardOutput: this.standardOutput,
					slug: this.slug,
					samples: this.samples,
					discussionvisible: this.discussionvisible,
					visible: this.visible,
				},
			})
				.then(() => {
					// location.reload();
				})
				.catch(error => this.$store.commit('snackbar/setSnack', error.message));
		},
		request() {
			this.$apollo.query({
				query: ProblemDetailGQL,
				variables: {
					slug: this.slug,
				},
			})
				.then(response => response.data.problem)
				.then((data) => {
					this.problem = Object.assign({}, data);
				});
		},
		has_permission(permission) {
			return this.$store.getters['user/has_permission'](permission);
		},
	},
};
</script>
