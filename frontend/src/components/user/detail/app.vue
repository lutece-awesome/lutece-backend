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
						<h3 class="headline">{{ getfield( 'username' ) }}</h3>
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
import { ProfileGQL } from '@/graphql/user/profile.gql';


export default {
	metaInfo() { return { title: this.username }; },

	components: {
		CalendarHeatmap,
	},
	data: () => ({
		HeatMapData: [],
		endDate: Date.now(),
		userdata: {},
	}),

	mounted() {
		this.$apollo.query({
			query: ProfileGQL,
			variables: {
				username: this.$route.params.username,
			},
		})
			.then(response => response.data.userProfile)
			.then((data) => {
				this.HeatMapData = JSON.parse(data.heatmap);
				this.userdata = data.user;
			});
	},

	methods: {
		getfield(field) {
			if (Object.prototype.hasOwnProperty.call(this.userdata, field)) {
				return this.userdata[field];
			}
			return '';
		},
	},
};
</script>
