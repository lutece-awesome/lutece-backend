<template>
	<div>
		<v-btn
			v-if = "$store.state.user.payload && username == $store.state.user.payload.username"
			:to = "{name: 'UserSettings'}"
			color = "accent"
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
								sm8
								md6
							>
								<UserProfile :user = "data.user" />
							</v-flex>
						</v-layout>
					</v-container>
					<v-container>

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
												<span style = "color:green" >
													{{ data.user.submissionStatistics.accept }}
												</span>
												<span> / </span>
												<span style = "color:red" >
													{{ data.user.submissionStatistics.accept
													+ data.user.submissionStatistics.reject }}
												</span>
											</span>
										</div>

										<div class = "mb-1" >
											<v-icon class = "mdi-18px" >mdi-check-all</v-icon>
											<span class = "ml-1 subheader" > Success Ratio </span>
											<span
												style = "float: right"
											>
												<span style = "color:green" >
													{{ successRatio(
														data.user.submissionStatistics.accept ,
														data.user.submissionStatistics.reject )
													}}%
												</span>
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
import LoadingSpinner from '@/components/basic/loading';
import DoughnutChart from '@/components/chart/doughnut';
import LineChart from '@/components/chart/line';
import UserProfile from '@/components/user/detail/profile';

export default {
	metaInfo() { return { title: this.username }; },

	components: {
		CalendarHeatmap,
		LoadingSpinner,
		DoughnutChart,
		LineChart,
		UserProfile,
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
			const ac = result.data.user.submissionStatistics.accept;
			const rj = result.data.user.submissionStatistics.reject;
			this.doughnutData = {
				labels: ['Accepted', 'Rejected'],
				datasets: [
					{
						backgroundColor: [
							'#21ba45',
							'red',
						],
						data: [ac, rj],
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
		successRatio(ac, rj) {
			const cnt = ac + rj;
			if (cnt === 0) return 0.0;
			return ((100.0 * ac) / cnt).toFixed(1);
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
