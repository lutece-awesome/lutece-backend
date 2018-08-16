<template>
	<v-container>
		<v-layout
			row
			wrap>
			<v-flex
				v-for = "( each , index ) in userItem"
				:key = "index"
				xs12
				sm6
			>
				<v-card
					:to = "{ name: 'UserDetail' , params: {username: each.username } }"
					hover
					class = "mb-4 mr-4 pt-4" >
					<v-layout
						row
						wrap>
						<v-flex xs4 >
							<v-card-media
								:src= "each.gravataremail"
								class = "card-avatar ml-4"
								height = "120px"
								contain/>
						</v-flex>
						<v-flex xs8>
							<div class = "ml-4" >
								<div class = "headline mb-1">
									{{ each.displayName }}
								</div>
								<div
									class = "mb-1"
									style = "overflow: hidden;white-space: nowrap;text-overflow: ellipsis;"
								>
									<v-icon class = "mdi-18px">mdi-school</v-icon>
									<span class = "ml-1"> {{ each.school }} </span>
								</div>
								<div
									class = "mb-1"
									style = "overflow: hidden;white-space: nowrap;text-overflow: ellipsis;"
								>
									<v-icon class = "mdi-18px">mdi-domain</v-icon>
									<span class = "ml-1"> {{ each.company }} </span>
								</div>
								<div
									class = "mb-1"
									style = "overflow: hidden;white-space: nowrap;text-overflow: ellipsis;"
								>
									<v-icon class = "mdi-18px">mdi-map-marker</v-icon>
									<span class = "ml-1"> {{ each.location }} </span>
								</div>
								<div class = "mb-1" >
									<v-icon class = "mdi-18px" >mdi-chart-bar</v-icon>
									<span class = "ml-1">
										<span style = "color:green" > {{ each.solved }} </span>
										/
										<span style = "color:red" > {{ each.tried }} </span>
									</span>
								</div>
							</div>
						</v-flex>
						<v-flex xs12>
							<v-divider class = "mt-2" />
						</v-flex>
						<v-flex
							xs12
							style = "overflow: hidden;white-space: nowrap;text-overflow: ellipsis;" >
							<v-list one-line>
								<v-list-tile>
									<v-list-tile-content>
										<v-list-tile-sub-title>
											<span class = "text--primary"> {{ each.about }} </span>
										</v-list-tile-sub-title>
									</v-list-tile-content>
								</v-list-tile>
							</v-list>
						</v-flex>
					</v-layout>
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
		isLoading: {
			type: Boolean,
			default: false,
		},
	},
};
</script>
