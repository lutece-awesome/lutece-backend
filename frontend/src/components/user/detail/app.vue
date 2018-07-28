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
				<v-card>
					<v-card-title primary-title>
						<h3 class="headline">{{ username }}</h3>
					</v-card-title>
					<v-card-text>
						<div class="scroll text-xs-center">
							<CalendarHeatmap
								:values = "HeatMapData"
								:end-date = "endDate"
								tooltip-unit = "submissions" />
						</div>
					</v-card-text>
				</v-card>
			</v-flex>

		</v-layout>
	</v-container>
</template>


<script>

import { CalendarHeatmap } from 'vue-calendar-heatmap';
import { HeatmapGQL } from '@/graphql/user/heatmap.gql';


export default {
	metaInfo() { return { title: this.username }; },

	components: {
		CalendarHeatmap,
	},
	data: () => ({
		username: '',
		HeatMapData: [],
		endDate: Date.now(),
	}),

	mounted() {
		this.username = this.$route.params.username;
		this.$apollo.query({
			query: HeatmapGQL,
			variables: {
				username: this.username,
			},
		})
			.then(response => response.data.userHeatmapData)
			.then((data) => { this.HeatMapData = JSON.parse(data); });
	},
};
</script>
