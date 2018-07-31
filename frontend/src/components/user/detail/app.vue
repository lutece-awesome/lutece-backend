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
					<v-avatar
						size="128"
						class="mr-2" >
						<img :src = "gravataremail">
					</v-avatar>
					<v-card-title primary-title>
						<h3 class="headline">{{ username }}</h3>
					</v-card-title>
					<v-card-text>
						<div> Activity </div>
						<div> <b> {{ total_submission }} </b> submissions during the last year. </div>
						<div class="scroll text-xs-center">
							<CalendarHeatmap
								:values = "heatmap"
								:end-date = "endDate"
								tooltip-unit = "submissions" />
						</div>
						<div> Solve </div>
						<v-btn
							v-for = "each in analysis"
							:color = "each[1] === 'yes' ? 'success' : 'error' "
							:key = "each[0]"
							round
							small
						>
							{{ each[0] }}
						</v-btn>
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
					this.heatmap = JSON.parse(this.heatmap);
					this.analysis = JSON.parse(this.analysis);
				});
		},
	},

};
</script>
