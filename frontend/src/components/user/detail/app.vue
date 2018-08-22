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
							<v-flex xs12 >
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
									:class = "{ 'smallprofilecard' : notxs }"
									hover
									class = "mt-2 profilecard"
								>
									<v-card-text>
										<h3>
											<v-icon class = "mdi-18px" >mdi-account </v-icon>
											<span class = "ml-1"> Profile </span>
										</h3>
										<v-divider class = "mt-2 mb-2" />
										<div class = "mb-1" >
											<v-icon class = "mdi-18px">mdi-school</v-icon>
											<span class = "ml-1"> {{ data.user.school }} </span>
										</div>
										<div class = "mb-1" >
											<v-icon class = "mdi-18px">mdi-domain</v-icon>
											<span class = "ml-1"> {{ data.user.company }} </span>
										</div>
										<div class = "mb-1" >
											<v-icon class = "mdi-18px">mdi-map-marker</v-icon>
											<span class = "ml-1"> {{ data.user.location }} </span>
										</div>
										<div class = "mb-1">
											<v-tooltip bottom>
												<span slot = "activator">
													<v-icon class = "mdi-18px">mdi-flag-variant</v-icon>
													<span class = "ml-1" >
														{{ data.user.lastloginDate | moment("from") }}
													</span>
												</span>
												<span>
													Last visited in
													{{ data.user.lastloginDate | moment("dddd, MMMM Do YYYY, h:mm:ss a") }}
												</span>
											</v-tooltip>
										</div>
										<div>
											<v-tooltip bottom>
												<span slot = "activator">
													<v-icon class = "mdi-18px">mdi-emoticon-cool</v-icon>
													<span class = "ml-1">
														{{ data.user.joinedDate | moment("from") }}
													</span>
												</span>
												<span>
													Joined in {{ data.user.lastloginDate | moment( "MMMM Do, YYYY" ) }}
												</span>
											</v-tooltip>
										</div>
									</v-card-text>
								</v-card>
							</v-flex>
						</v-layout>

						<v-layout
							row
							wrap
						>

							<v-flex xs12>
								<v-card
									:class = "{ 'smallchartcard' : notxs }"
									hover
									class = "mt-4 chart"
									style = "cursor:default; margin: 0 auto;"
								>
									<v-card-text>
										<h3>
											<v-icon class = "mdi-18px" >mdi-octagram-outline </v-icon>
											<span class = "ml-1">  Summary </span>
										</h3>
										<v-divider class = "mt-2 mb-2" />
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
											<v-icon class = "mdi-18px" >mdi-view-list</v-icon>
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

										<DoughnutChart
											:data = "doughnutData"
											:options = "doughnutOptions"
										/>
									</v-card-text>
								</v-card>
							</v-flex>

							<v-flex xs12>
								<v-card
									:class = "{ 'smallchartcard' : notxs }"
									hover
									class = "mt-4 chart"
									style = "cursor:default; margin: 0 auto;"
								>
									<v-card-text>
										<h3>
											<v-icon class = "mdi-18px" >mdi-chart-donut </v-icon>
											<span class = "ml-1">  Recently Progress </span>
										</h3>
										<v-divider class = "mt-2 mb-2" />
										<LineChart
											:data = "lineData"
											:options = "lineOptions"
										/>
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
import DoughnutChart from '@/components/chart/doughnut';
import LineChart from '@/components/chart/line';

export default {
	metaInfo() { return { title: this.username }; },

	components: {
		CalendarHeatmap,
		LoadingSpinner,
		DoughnutChart,
		LineChart,
	},

	data: () => ({
		doughnutData: null,
		barData: null,
		doughnutOptions: {
			responsive: true,
			maintainAspectRatio: false,
		},
		lineOptions: {
			responsive: true,
			maintainAspectRatio: false,
		},
	}),

	computed: {
		username() {
			return this.$route.params.username;
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
			this.doughnutData = {
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

			this.lineData = {
				labels: ['1st, Aug', '2st Feb', '3nd Jan', '1st, Aug', '1st, Aug', '1st, Aug', '1st, Aug', '1st, Aug', '1st, Aug', '1st, Aug', '1st, Aug', '1st, Aug', '1st, Aug', '1st, Aug'],
				datasets: [
					{
						label: 'Submissions',
						backgroundColor: '#e87979',
						data: [1, 2, 3, 4, 4, 3, 2, 1, 5, 6, 7, 4, 3, 5],
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

	.profilecard{
		cursor: default;
		margin: 0 auto;
	}

	.smallprofilecard{
		width: 50%;
	}

	.smallchartcard{
		width: 60%;
	}
</style>
