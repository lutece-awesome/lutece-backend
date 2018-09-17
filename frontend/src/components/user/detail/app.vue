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
								sm6
								style = "min-height: 164px;"
							>
								<UserProfile :user = "data.user"/>
							</v-flex>
							<v-flex
								:class = "{
									'mt-4': $vuetify.breakpoint.xsOnly,
									'pl-4': !$vuetify.breakpoint.xsOnly
								}"
								xs12
								sm6
								style = "min-height: 164px;"
							>
								<UserRank
									:rank = "data.user.rank"
									:solved = "data.user.solved"
									:tried = "data.user.tried"
								/>
							</v-flex>
						</v-layout>
					</v-container>

					<v-container>
						<v-layout
							row
							wrap
						>

							<v-flex
								xs12
								sm6
							>
								<UserSummary :statistics = "data.user.submissionStatistics"/>
							</v-flex>

							<!-- <v-flex
								xs12
								sm6>
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
							</v-flex> -->


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
import LineChart from '@/components/chart/line';
import UserProfile from '@/components/user/detail/profile';
import UserRank from '@/components/user/detail/rank';
import UserSummary from '@/components/user/detail/summary';

export default {
	metaInfo() { return { title: this.username }; },

	components: {
		CalendarHeatmap,
		LoadingSpinner,
		LineChart,
		UserProfile,
		UserRank,
		UserSummary,
	},

	data: () => ({
		barData: null,
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
			console.log(result);
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
