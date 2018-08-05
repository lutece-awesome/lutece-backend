<template>
	<v-card
		:class = "{ 'ml-5' : isReply }"
		class = "mt-2"
	>
		<div class = "pl-1 pr-1" >
			<v-card-text
				class = "mb-4" >
				<div>
					<v-avatar size = "40" >
						<img :src = "value.user.gravataremail" >
					</v-avatar>
					<router-link
						:to = "{name: 'UserDetail', params: {username: value.user.username}}"
						class = "ml-2"
					>
						{{ value.user.displayName }}
					</router-link>
					<span
						class = "ml-2"
						style = "color:#999;" >
						<v-icon small>
							mdi-clock-outline
						</v-icon>
						<span class="humanize-time">
							{{ value.submitTime | moment("from") }}
						</span>
						<span class="full-time">
							{{ value.submitTime | moment("Y-MM-DD HH:mm:ss") }}
						</span>
					</span>
				</div>
				<div
					v-mixrend = "value.content"
					class = "mt-3"/>
				<div
					class = "mb-0 mt-2"
					style = "color:#999;">
					<span
						class = "display-0" >
						{{ value.vote }}
					</span>
					<span class = "ml-1" >
						<a>
							<v-icon
								:color = "value.hasVoted === true ? 'green darkgen-2' : 'grey' "
								small
							>
								mdi-chevron-up
							</v-icon>
						</a>
					</span>
					<span>
						<a>
							<v-icon
								:color = "value.hasVoted === false ? 'green darkgen-2' : 'grey' "
								small
							>
								mdi-chevron-down
							</v-icon>
						</a>
					</span>
					<span class = "ml-2 mr-2" > | </span>
					<a style = "color:#999">
						Reply
					</a>
				</div>
			</v-card-text>
		</div>
	</v-card>
</template>


<script>
export default {
	props: {
		value: {
			type: Object,
			default: () => ({
				user: {
					displayName: '',
					username: '',
					gravataremail: '',
				},
				pk: 0,
				submitTime: 0,
				hasVoted: false,
				vote: 0,
				content: '',
			}),
		},
		isReply: {
			type: Boolean,
			default: false,
		},
	},
};
</script>

<style scoped>
	.v-card:hover{
		box-shadow: 3px 3px 3px #888888;
	}
</style>
