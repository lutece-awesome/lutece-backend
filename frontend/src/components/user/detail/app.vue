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
						<img :src = "gravataremail" >
					</v-avatar>
					<v-card-title primary-title>
						<h3 class="headline">{{ username }}</h3>
					</v-card-title>
					<v-card-text>
						<div class="scroll text-xs-center">
							<CalendarHeatmap
								:values = "heatmap"
								:end-date = "endDate"
								tooltip-unit = "submissions" />
						</div>
					</v-card-text>
					<v-btn
						v-for = "each in analysis"
						:key = "each[0]"
					>
						{{ each[0] }}
						{{ each[1] }}
					</v-btn>
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
		username: '',
		displayName: '',
		gravataremail: '',
		group: '',
		school: '',
		company: '',
		location: '',
		about: '',
	}),

	mounted() {
		this.$apollo.query({
			query: ProfileGQL,
			variables: {
				username: this.$route.params.username,
			},
		})
			.then(response => response.data.user)
			.then((data) => {
				Object.assign(this, data);
				this.heatmap = JSON.parse(this.heatmap);
				this.analysis = JSON.parse(this.analysis);
			});
	},

};
</script>
