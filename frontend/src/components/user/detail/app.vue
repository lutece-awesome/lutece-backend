<template>
	<div>
		<v-btn
			v-if="$store.state.user.payload && username == $store.state.user.payload.username"
			:to="{name: 'UserSettings'}"
			color="accent"
			dark
			fab
			fixed
			bottom
			right>
			<v-icon>mdi-pencil</v-icon>
		</v-btn>
		<ApolloQuery
			:query = "require('@/graphql/user/profile.gql')"
			:variables = "{ username }"
			@result = "onResult"
		>
			<template
				slot-scope = "{ result: { loading , error , data } }">
				<div v-if = "loading" >
					<LoadingSpinner />
				</div>
				<div v-else-if = "error" >An error occured</div>
				<div v-else-if = "data" >
					<v-container>
						<v-layout
							row
							wrap
						>
							<v-flex
								xs12
								sm4
								align-content-start
							>
								<div
									:class = "{'mb-2': $vuetify.breakpoint.xsOnly}"
									class = "text-xs-center mt-2">
									<v-avatar
										size = "128"
										class = "mt-2"
									>
										<img :src = "data.user.gravataremail" >
									</v-avatar>
									<h3 class = "mt-2"> {{ data.user.displayName }} </h3>
								</div>
								<v-card
									hover
									class = "mt-2"
									style = "cursor:default;"
								>
									<v-card-text>
										<div class = "mb-1" >
											<v-icon class = "mdi-18px">mdi-school</v-icon>
											<span class = "ml-1"> {{ data.user.school }} </span>
										</div>
										<div class = "mb-1" >
											<v-icon class = "mdi-18px">mdi-domain</v-icon>
											<span class = "ml-1"> {{ data.user.company }} </span>
										</div>
										<div>
											<v-icon class = "mdi-18px">mdi-map-marker</v-icon>
											<span class = "ml-1"> {{ data.user.location }} </span>
										</div>
									</v-card-text>
								</v-card>
								<v-card
									hover
									class = "mt-4"
									style = "cursor:default;"
								>
									<v-card-text>
										<div class = "mb-1" >
											<v-icon class = "mdi-18px" >mdi-chart-bar</v-icon>
											<span class = "ml-1 subheader" > Solved Problem </span>
											<span
												style = "float: right"
											>
												<span style = "color:green" > {{ data.user.solved }} </span>
												<span> / </span>
												<span style = "color:red" > {{ data.user.tried }} </span>
											</span>
										</div>

										<div class = "mb-1" >
											<v-icon class = "mdi-18px" >mdi-nut</v-icon>
											<span class = "ml-1 subheader" > Submission Analysis </span>
											<span
												style = "float: right"
											>
												<span style = "color:green" > 50 </span>
												<span> / </span>
												<span style = "color:red" > 932 </span>
											</span>
										</div>

										<div class = "mb-1" >
											<v-icon class = "mdi-18px" >mdi-check-all</v-icon>
											<span class = "ml-1 subheader" > Success Ratio </span>
											<span
												style = "float: right"
											>
												<span style = "color:green" > 5.4% </span>
											</span>
										</div>

										<v-divider class = "mt-2 mb-2" />
										<Doughnut
											:data = "chartData"
											:options = "chartOptions"
										/>
									</v-card-text>
								</v-card>
							</v-flex>

							<v-flex
								:class = "{ 'mt-4' : isxs , 'pl-4' : notxs }"
								xs12
								sm8
							>
								<v-card
									hover
									style = "cursor: default;"
								>
									<v-card-text>
										123
									</v-card-text>
								</v-card>
							</v-flex>
						</v-layout>
					</v-container>
				</div>
			</template>
		</ApolloQuery>
	</div>
</template>


<script>

import { CalendarHeatmap } from 'vue-calendar-heatmap';
import LoadingSpinner from '@/components/basic/loadingspinner';
import Doughnut from '@/components/user/detail/doughnut';


export default {
	metaInfo() { return { title: this.username }; },

	components: {
		CalendarHeatmap,
		LoadingSpinner,
		Doughnut,
	},

	data: () => ({
		chartData: null,
	}),

	computed: {
		username() {
			return this.$route.params.username;
		},
		chartOptions() {
			return { responsive: true, maintainAspectRatio: false };
		},
		isxs() {
			return this.$vuetify.breakpoint.smAndDown;
		},
		notxs() {
			return !this.$vuetify.breakpoint.smAndDown;
		},
	},

	methods: {
		onResult(result) {
			this.chartData = {
				labels: ['Accepted', 'Rejected'],
				datasets: [
					{
						backgroundColor: [
							'#21ba45',
							'red',
						],
						data: [result.data.user.solved, result.data.user.tried],
					},
				],
			};
		},
	},
};
</script>


<style scoped>
	.subheader{
		font-weight: 500;
	}
</style>
