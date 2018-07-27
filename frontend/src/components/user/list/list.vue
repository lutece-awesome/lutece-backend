<template>
	<v-container
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
