<template>
	<div>
		<v-card
			:class = "{ 'ml-5' : isReply }"
			class = "mt-2"
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
							<span class="humanize-time">
								{{ data.submitTime | moment("from") }}
							</span>
							<span class="full-time">
								{{ data.submitTime | moment("Y-MM-DD HH:mm:ss") }}
							</span>
						</span>
					</div>
					<div
						v-mixrend = "data.content"
						class = "mt-3 commentContent"/>
					<div
						class = "mb-0 mt-2"
						style = "color:#999;">
						<span
							class = "display-0" >
							{{ data.vote }}
						</span>
						<span class = "ml-1" >
							<a
								@click = "voteDiscussion( true )"
							>
								<v-icon
									:color = "data.attitude === 'Agree' ? 'green darkgen-2' : 'grey' "
									small
								>
									mdi-chevron-up
								</v-icon>
							</a>
						</span>
						<span>
							<a
							>
								<v-icon
									:color = "data.attitude === 'Disagree' ? 'green darkgen-2' : 'grey' "
									small
									@click = "voteDiscussion( false )"
								>
									mdi-chevron-down
								</v-icon>
							</a>
						</span>
						<span class = "ml-2 mr-2" > | </span>
						<a
							style = "color:#999"
							@click = "Reply" >
							Reply
						</a>
					</div>
				</v-card-text>
			</div>
		</v-card>
		<textEditor />
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
			alert(this.replycontent);
		},

		voteDiscussion(attitude) {
			if (!this.isAuthenticated) return;
			if (this.uploading) {
				alert('Please wait a moment...');
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
	},
};
</script>

<style scoped>
	.v-card:hover{
		box-shadow: 3px 3px 3px #888888;
	}
</style>
