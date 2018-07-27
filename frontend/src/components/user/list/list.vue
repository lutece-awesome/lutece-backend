<template>
	<v-container
		class="pa-0"
		fluid
		grid-list-lg>
		<v-layout
			row
			wrap
		>
			<v-flex
				v-for="each in userItem"
				:key="each.displayName"
				xs12
				sm6
				md4
				xl3>
				<v-card :to="{name: 'UserDetail', params: {username: each.username}}">
					<v-layout
						class="ma-0">
						<v-flex
							xs5>
							<v-card-media
								:src="each.gravataremail"
								class="card-avatar"
								height="125px"
								contain
							/>
						</v-flex>
						<v-flex
							xs7
							class="pa-0">
							<v-card-title>
								<div>
									<div
										class="headline"
										style="text-overflow: ellipsis;overflow: hidden;">{{ each.displayName }}</div>
									<div v-if="each.school">
										<v-icon class="mdi-18px">mdi-school</v-icon> {{ each.school }}
									</div>
									<div v-if="each.company">
										<v-icon class="mdi-18px">mdi-domain</v-icon> {{ each.company }}
									</div>
									<div v-if="each.location">
										<v-icon class="mdi-18px">mdi-map-marker</v-icon> {{ each.location }}
									</div>
								</div>
							</v-card-title>
						</v-flex>
					</v-layout>
					<v-divider/>
					<v-card-text
						v-if="each.about">
						<div
							v-line-clamp:21="4"
							class="user-about"
							v-html="$options.filters.nl2br(each.about)"/>
					</v-card-text>
				</v-card>
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>
export default {
	props: {
		userItem: {
			type: Array,
			default: () => [],
		},
	},
};
</script>
