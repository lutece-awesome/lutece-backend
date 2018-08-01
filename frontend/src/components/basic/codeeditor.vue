<template>
	<v-layout
		v-resize="onResize"
		row
		wrap>
		<v-flex xs12>
			<codemirror
				v-model="code"
				:options="cmOptions"
				:style="cmHeight"
			/>
		</v-flex>
		<v-flex xs12>
			<v-divider/>
		</v-flex>
		<v-flex xs12>
			<v-card-actions>
				<v-spacer/>
				<v-select
					v-model="language"
					:items="items"
					offset-y
					solo
					flat
					hide-details
					class="shrink"
				/>
				<v-btn
					large
					flat
					color="primary"
					type="submit"
					@click= "submitsolution" >Submit</v-btn>
			</v-card-actions>
		</v-flex>
	</v-layout>
</template>

<script>
import { LanguageList } from '@/graphql/language/languagelist.gql';
import { SubmitSolution } from '@/graphql/submission/submit.gql';
import { mapGetters } from 'vuex';


export default {

	components: {
		codemirror: () => import('./codemirror'),
	},
	props: {
		problemslug: {
			type: String,
			required: true,
		},
	},
	data: () => ({
		cmOptions: {
			indentUnit: 4,
			lineNumbers: true,
			keyMap: 'sublime',
			tabindex: '0',
			line: true,
			styleActiveLine: true,
			matchBrackets: true,
			scrollbarStyle: 'overlay',
			mode: '',
			theme: 'neo',
			autoRefresh: true,
		},
		code: '',
		language: '',
		items: [],
		height: 0,
	}),
	computed: {
		cmHeight() {
			return `height: ${this.height}px`;
		},
		...mapGetters({
			isAuthenticated: 'user/isAuthenticated',
		}),
	},
	watch: {
		language() {
			for (let i = 0; i < this.items.length; i += 1) {
				if (this.items[i].value === this.language) {
					this.cmOptions.mode = this.items[i].codemirror;
				}
			}
		},
	},

	mounted() {
		this.onResize();
		this.$apollo.query({
			query: LanguageList,
		})
			.then(response => response.data.allLanguage)
			.then((data) => {
				this.data = [];
				for (let i = 0; i < data.length; i += 1) {
					const {
						full, info,
					} = data[i];
					this.items.push({ text: info, value: full, codemirror: data[i].codemirror });
				}
				this.language = this.items[0].value;
			});
	},
	methods: {
		onResize() {
			this.height = Math.max(window.innerHeight - 300, 300);
		},
		submitsolution() {
			if (!this.isAuthenticated) {
				this.$router.push({
					name: 'Login',
					query: {
						redirect: this.$route.path,
					},
				});
				return;
			}
			this.$apollo.mutate({
				mutation: SubmitSolution,
				variables: {
					code: this.code,
					language: this.language,
					problemslug: this.problemslug,
				},
			}).then(response => response.data.SubmitSolution)
				.then((data) => {
					this.$router.push({
						name: 'StatusDetail',
						params: {
							pk: data.pk,
						},
					});
				})
				.catch((error) => {
					this.$store.commit('snackbar/setSnack', error.message);
				});
		},
	},

};
</script>
