<template>
	<div>
		<v-card
			:class = "{ 'ml-5' : isReply }"
			hover
			class = "mt-2 card"
		>
			<div class = "pl-1 pr-1" >
				<v-card-text
					class = "mb-4" >
					<div>
						<v-avatar size = "40" >
							<img :src = "data.user.gravataremail" >
						</v-avatar>
						<router-link
							:to = "{name: 'UserDetail', params: {username: data.user.username}}"
							class = "ml-2"
						>
							{{ data.user.displayName }}
						</router-link>
						<span
							class = "ml-2"
							style = "color:#999;" >
							<v-icon small>
								mdi-clock-outline
							</v-icon>
							<span
								:title = "data.submitTime | moment('Y-MM-DD HH:mm:ss')"
								class="humanize-time" >
								{{ data.submitTime | moment("from") }}
							</span>
						</span>
					</div>
					<div
						v-mixrend = "data.content"
						class = "mt-3 commentContent"/>
					<div
						class = "mb-0 mt-2 subheader"
					>
						<span> {{ data.vote }} </span>
						<span class = "ml-1" >
							<v-icon
								:color = "data.attitude === 'Agree' ? 'green darkgen-2' : 'grey' "
								@click = "voteDiscussion( true )"
							>
								mdi-chevron-up
							</v-icon>
						</span>
						<span>
							<v-icon
								:color = "data.attitude === 'Disagree' ? 'red darkgen-2' : 'grey' "
								@click = "voteDiscussion( false )"
							>
								mdi-chevron-down
							</v-icon>
						</span>
						<span class = "ml-2 mr-2" > | </span>
						<span
							style = "cursor:pointer;"
							@click = "Reply" >
							Reply
						</span>
					</div>
				</v-card-text>
			</div>
		</v-card>
		<textEditor
			:class = "{ 'ml-5' : isReply }"
			:display = "editorDisplay"
			@close-editor = "closeEditor" />
	</div>
</template>


<script>
import { mapGetters } from 'vuex';
import textEditor from '@/components/basic/texteditor';
import VoteDiscussionGQL from '@/graphql/votediscussion/vote.gql';

export default {

	components: {
		textEditor,
	},

	props: {
		value: {
			type: Object,
			default: () => null,
		},
		isReply: {
			type: Boolean,
			default: false,
		},
	},

	data: () => ({
		data: {
			user: {
				displayName: '',
				username: '',
				gravataremail: '',
			},
			pk: 0,
			submitTime: 0,
			attitude: 'Neutral',
			vote: 0,
			content: '',
		},
		editorDisplay: false,
	}),

	computed: {
		...mapGetters({
			isAuthenticated: 'user/isAuthenticated',
		}),
	},

	created() {
		this.data = JSON.parse(JSON.stringify(this.value));
	},

	methods: {
		Reply() {
			if (!this.isAuthenticated) {
				this.$router.push({
					name: 'Login',
					query: {
						redirect: this.$route.path,
					},
				});
				return;
			}
			this.editorDisplay = true;
		},

		voteDiscussion(attitude) {
			if (!this.isAuthenticated) {
				this.$router.push({
					name: 'Login',
					query: {
						redirect: this.$route.path,
					},
				});
				return;
			}
			if (this.uploading) {
				this.$store.commit('snackbar/setSnack', 'Please wait a moment...');
				return;
			}
			this.uploading = true;
			this.$apollo.mutate({
				mutation: VoteDiscussionGQL,
				variables: {
					pk: this.data.pk,
					attitude,
				},
			})
				.then(response => response.data.UpdateDiscussionVote)
				.then((data) => {
					this.data.attitude = data.result;
					this.data.vote = data.vote;
				})
				.finally(() => { this.uploading = false; });
		},

		closeEditor() {
			this.editorDisplay = false;
		},
	},
};
</script>

<style scoped>
	.subheader {
		font-size: 16px;
		font-weight:  350;
	}

	.card {
		cursor: default;
	}
</style>
