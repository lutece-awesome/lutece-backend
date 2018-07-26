<template>
	<v-container
		:class="{'pa-3': $vuetify.breakpoint.xsOnly}"
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
				<v-card>
					<v-layout>
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
						{{ each.about }}
					</v-card-text>
					<v-divider/>
					<v-card-actions>
						<v-spacer/>
						<v-btn
							flat
							color="primary">
							Follow
						</v-btn>
					</v-card-actions>
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
