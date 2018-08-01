<template>
	<v-container
		:class="{'pa-0': $vuetify.breakpoint.xsOnly }"
		fluid>
		<v-layout
			row
			justify-center>
			<v-flex
				xs12
				md8>
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
				<v-card>
					<div
						:class="{'mb-2': $vuetify.breakpoint.xsOnly}"
						class="text-xs-center mt-2">
						<v-avatar
							size="128"
							class="mr-2" >
							<img :src = "gravataremail" >
						</v-avatar>
					</div>

					<h2
						class="text-xs-center mt-2"
					>{{ displayName }}
					</h2>

					<v-card-text>
						<h3> Activity </h3>
						<p> <b> {{ total_submission }} </b> submissions during the last year. </p>
						<div class="scroll text-xs-center">
							<CalendarHeatmap
								:values = "heatmap"
								:end-date = "endDate"
								tooltip-unit = "submissions" />
						</div>
						<h3> Detail </h3>
						<router-link
							v-for = "each in analysis"
							:key = "each[0]"
							:to = "{name: 'ProblemDetailDescription', params: {slug: each[2]}}">
							<v-btn
								:color = "each[1] === 'yes' ? 'success' : 'error' "
								round
								small
							>
								{{ each[0] }}
							</v-btn>
						</router-link>
					</v-card-text>
				</v-card>
			</v-flex>

		</v-layout>
	</v-container>
</template>


<script>

import { CalendarHeatmap } from 'vue-calendar-heatmap';
import { ProfileGQL } from '@/graphql/user/profile.gql';


export default {
	metaInfo() { return { title: this.username }; },

	components: {
		CalendarHeatmap,
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
