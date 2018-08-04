<template>
	<div>
		<v-card
			v-for = "( discussion , index ) in value"
			:key = "index"
			class = "mt-2 ml-4" >
			<div class = "pl-1 pr-1" >
				<v-card-text
					class = "mb-4" >
					<div>
						<v-avatar size = "40" >
							<img :src = "discussion.user.gravataremail" >
						</v-avatar>
						<router-link
							:to = "{name: 'UserDetail', params: {username: discussion.user.username}}"
							class = "ml-1"
						>
							{{ discussion.user.displayName }}
						</router-link>
						<span
							class = "ml-2"
							style = "color:#999;" >
							<v-icon small>
								mdi-clock-outline
							</v-icon>
							<span class="humanize-time">
								{{ discussion.submitTime | moment("from") }}
							</span>
							<span class="full-time">
								{{ discussion.submitTime | moment("Y-MM-DD HH:mm:ss") }}
							</span>
						</span>
					</div>
					<div
						v-mixrend = "discussion.content"
						class = "mt-3"/>
					<div
						class = "mb-0 mt-2"
						style = "color:#999;">
						<span> {{ discussion.vote }} </span>
						<span class = "ml-1" >
							<v-icon
								small
								green>
								mdi-chevron-up
							</v-icon>
						</span>
						<span>
							<v-icon small>
								mdi-chevron-down
							</v-icon>
						</span>
						<span class = "ml-2 mr-2" > | </span>
						<span> Reply </span>
					</div>
				</v-card-text>
			</div>
		</v-card>
	</div>
	<!-- <v-card class = "ml-5">
				<div class = "pl-1 pr-1" >
					<v-card-text
						class = "mb-4" >
						<div>
							<v-avatar size = "40" >
								<img src = "https://secure.gravatar.com/avatar/79bc21937a1f625d1cf08c919f8c70c2.jpg?r=g&s=300&d=mm" >
							</v-avatar>
							<a class = "ml-1" > xiper </a>
							<span
								class = "ml-2"
								style = "color:#999;" >
								<v-icon small>
									mdi-clock-outline
								</v-icon>
								5 hours ago
							</span>
						</div>
						<div class = "mt-3">
							BioShock Infinite is a first-person shooter video game de
							veloped by Irrational Games and published by 2K Games. It was re
							leased worldwide for the Microsoft Windows, PlayStation 3, and Xbox 360
							platforms on March 26, 2013; an OS X port by Aspyr was later released on
							August 29, 2013 and a Linux port was released on March 17, 2015. Infinite is th
							e third installment in the BioShock series, and though it is not immediately part of
							the storyline of previous BioShock games, it features similar gameplay
						</div>
						<div
							class = "mb-0 mt-2"
							style = "color:#999;">
							<span> 5 </span>
							<span class = "ml-1" >
								<v-icon small>
									mdi-chevron-up
								</v-icon>
							</span>
							<span>
								<v-icon small>
									mdi-chevron-down
								</v-icon>
							</span>
							<span class = "ml-2 mr-2" > | </span>
							<span> Reply </span>
						</div>
					</v-card-text>
				</div>
			</v-card>
		</div>
	</div> -->
</template>

<script>
export default {
	props: {
		value: {
			type: Array,
			default: () => ([]),
		},
	},
};
</script>
