<template>
	<v-hover>
		<v-card
			slot-scope = "{ hover }"
			:class = "`elevation-${hover ? 4 : 1}`"
		>
			<v-container>
				<v-layout
					row
					wrap>

					<v-flex xs12>
						<h3>
							<v-icon class = "mdi-18px" >mdi-octagram-outline </v-icon>
							<span class = "ml-1">  Summary </span>
						</h3>
						<v-divider class = "mt-2 mb-3" />
					</v-flex>
					<v-flex xs12>
						<div class = "mb-1" >
							<v-icon class = "mdi-18px" >mdi-view-list</v-icon>
							<span class = "ml-1 subheader" > Total Submissions </span>
							<span
								style = "float: right"
							>
								<span style = "color:green" >
									{{ accept }}
								</span>
								<span> / </span>
								<span style = "color:red" >
									{{ all }}
								</span>
							</span>
						</div>

						<div class = "mb-1 mt-1" >
							<v-icon class = "mdi-18px" >mdi-check-all</v-icon>
							<span class = "ml-1 subheader" > Success Ratio </span>
							<span
								style = "float: right"
							>
								<span style = "color:green" >
									{{ successRatio( accept , all ) }} %
								</span>
							</span>
						</div>

						<Bar
							:data = "data"
							:options = "options"
						/>
					</v-flex>
				</v-layout>
			</v-container>
		</v-card>
	</v-hover>
</template>


<script>

import Bar from '@/components/chart/bar';

export default {
	components: {
		Bar,
	},
	props: {
		statistics: {
			type: Object,
			default: null,
		},
		options: {
			type: Object,
			default: () => ({}),
		},
	},
	data: () => ({
		data: null,
	}),
	computed: {
		accept() {
			return this.statistics.ac;
		},
		all() {
			let sum = 0;
			Object.keys(this.statistics).forEach((key) => {
				const value = this.statistics[key];
				if (Number.isInteger(value)) {
					sum += value;
				}
			});
			return sum;
		},
	},
	mounted() {
		Object.keys(this.statistics).forEach((key) => {
			const value = this.statistics[key];
			if (Number.isInteger(value)) {

			}
		});
	},
	methods: {
		successRatio(ac, all) {
			if (all === 0) return 0.0;
			return ((100.0 * ac) / all).toFixed(1);
		},
	},
};
</script>
