<template>
	<v-container
		:class="{'pa-0': $vuetify.breakpoint.xsOnly }"
		fluid>
		<v-layout
			row
			wrap
			justify-center>
			<v-flex
				xs12
				md10
				xl8>
				<v-btn
					v-if="hasPermission('problem.change_problem')"
					:to="{name: 'ProblemEdit', params: {slug: slug}}"
					color="accent"
					dark
					fab
					fixed
					bottom
					right>
					<v-icon>mdi-pencil</v-icon>
				</v-btn>
				<v-card>
					<v-tabs
						v-if="problem"
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
					</v-tabs>
					<v-tabs-items
						v-if="problem"
						v-model="tabs"
						touchless>
						<v-tab-item id="description">
							<ProblemDescription :problem = "problem"/>
						</v-tab-item>
						<v-tab-item id="editor">
							<ProblemEditor :problemslug = "slug" />
						</v-tab-item>
						<v-tab-item id="discussion">
							<ProblemDiscussion/>
						</v-tab-item>
					</v-tabs-items>
				</v-card>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
import ProblemDescription from '@/components/problem/detail/description';
import ProblemEditor from '@/components/problem/detail/editor';
import ProblemDiscussion from '@/components/problem/detail/discussion';
import ProblemDetailGQL from '@/graphql/problem/detail.gql';
import { mapGetters } from 'vuex';

export default {
	metaInfo() { return { title: this.problem ? this.problem.title : 'Loading...' }; },
	components: {
		ProblemDescription,
		ProblemEditor,
		ProblemDiscussion,
	},
	data: () => ({
		slug: '',
		isLoading: false,
		tabs: null,
		problem: null,
	}),

	computed: {
		...mapGetters({
			hasPermission: 'user/hasPermission',
		}),
	},

	created() {
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
					this.problem = data;
				});
		},
	},
};
</script>
