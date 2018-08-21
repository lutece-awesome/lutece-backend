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
		>
			<template
				slot-scope = "{ result: { loading , error , data } }">
				<div v-if = "loading" >
					<LoadingSpinner />
				</div>
				<div v-else-if = "error" >An error occured</div>
				<div v-else-if = "data" >
					<v-container
						:class="{'pa-0': $vuetify.breakpoint.xsOnly }"
						fluid>
						<v-layout
							row
							wrap
						>
							<v-flex
								xs12
								md4
								align-content-start
							>
								<div
									:class="{'mb-2': $vuetify.breakpoint.xsOnly}"
									class="text-xs-center mt-2">
									<v-avatar
										size = "128"
										class = "mt-2"
									>
										<img :src = "data.user.gravataremail" >
									</v-avatar>
								</div>
								<v-card
									hover
									class = "mt-2"
									style = "cursor:default;"
								>
									<v-card-text>
										<div class = "mb-1" >
											<v-icon class = "mdi-18px">mdi-account</v-icon>
											<span class = "ml-1"> {{ data.user.displayName }} </span>
										</div>
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
										<!-- <div>
											<v-icon class = "mdi-18px" >mdi-chart-bar</v-icon>
											<span class = "ml-1">
												<span style = "color:green" > {{ data.user.solved }} </span>
												/
												<span style = "color:red" > {{ data.user.tried }} </span>
											</span>
										</div> -->
									</v-card-text>
								</v-card>
								<v-card
									hover
									class = "mt-4"
									style = "cursor:default;"
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
import { ProfileGQL } from '@/graphql/user/profile.gql';
import LoadingSpinner from '@/components/basic/loadingspinner';


export default {
	metaInfo() { return { title: this.username }; },

	components: {
		CalendarHeatmap,
		LoadingSpinner,
	},

	data: () => ({
		endDate: Date.now(),
		heatmap: [],
		analysis: [],
		displayName: '',
		gravataremail: '',
		group: '',
		school: '',
		company: '',
		location: '',
		about: '',
		solved: 0,
		tried: 0,
	}),

	computed: {
		username() {
			return this.$route.params.username;
		},
		total_submission() {
			let sum = 0;
			for (let i = 0; i < this.heatmap.length; i += 1) {
				sum += this.heatmap[i].count;
			}
			return sum;
		},
	},

	watch: {
		username() {
			this.request();
		},
	},

	mounted() {
		this.request();
	},

	methods: {
		request() {
			this.$apollo.query({
				query: ProfileGQL,
				variables: {
					username: this.username,
				},
			})
				.then(response => response.data.user)
				.then((data) => {
					Object.assign(this, data);
				});
		},
	},

};
</script>
