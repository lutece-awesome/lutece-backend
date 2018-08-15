<template>
	<!-- <v-container
		class="pa-0"
		fluid
		grid-list-lg>
		<v-data-iterator
			:items="userItem"
			:loading="isLoading"
			content-tag="v-layout"
			hide-actions
			row
			wrap
		>
			<v-flex
				slot="item"
				slot-scope="props"
				xs12
				sm6
				md4
				lg3
			>
				<v-card :to="{name: 'UserDetail', params: {username: props.item.username}}">
					<v-layout
						class="ma-0">
						<v-flex
							xs5>
							<v-card-media
								:src="props.item.gravataremail"
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
										style="text-overflow: ellipsis;overflow: hidden;">
										{{ props.item.displayName }}
									</div>
									<div v-if="props.item.school">
										<v-icon class="mdi-18px">mdi-school</v-icon> {{ props.item.school }}
									</div>
									<div v-if="props.item.company">
										<v-icon class="mdi-18px">mdi-domain</v-icon> {{ props.item.company }}
									</div>
									<div v-if="props.item.location">
										<v-icon class="mdi-18px">mdi-map-marker</v-icon> {{ props.item.location }}
									</div>
								</div>
							</v-card-title>
						</v-flex>
					</v-layout>
					<v-divider/>
					<v-card-text
						v-if="props.item.about">
						<div
							v-line-clamp:21="4"
							class="user-about"
							v-html="$options.filters.nl2br(props.item.about)"/>
					</v-card-text>
				</v-card>
			</v-flex>
		</v-data-iterator>
	</v-container> -->
	<v-container>
		<v-layout row wrap>
			<v-flex
				v-for = "( each , index ) in userItem" 
				:key = "index"
				xs12
				sm6
				md4
				lg3>
			<v-card 
				hover 
				:to = "{ name: 'UserDetail' , params: {username: each.username } }"
				class = "mb-4 mr-4 pt-4" >
				<v-layout row wrap>
					<v-flex xs4>
						<v-card-media
							class = "card-avatar"
							height = "64px"
							:src=  "each.gravataremail"
							contain
						>
						</v-card-media>
					</v-flex>
					<v-flex xs8>
						<v-card-tile>
							<div class = "ml-2" >
								<div
									class = "headline mb-1"
									style = "text-overflow: ellipsis;overflow: hidden;">
									{{ each.displayName }}
								</div>
								<div v-if = "each.school" class = "mb-1" >
									<v-icon class="mdi-18px">mdi-school</v-icon>
									<span class = "ml-1"> {{ each.school }} </span>
								</div>
								<div v-if = "each.company" class = "mb-1" >
									<v-icon class="mdi-18px">mdi-domain</v-icon>
									<span class = "ml-1"> {{ each.company }} </span>
								</div>
								<div v-if = "each.location" class = "mb-1" >
									<v-icon class="mdi-18px">mdi-map-marker</v-icon>
									<span class = "ml-1"> {{ each.location }} </span>
								</div>
							</div>
						</v-card-tile>
					</v-flex>
					<v-flex xs12>
						<v-divider class = "mt-2" />
					</v-flex>
					<v-flex xs12>
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


<style scoped>
</style>
