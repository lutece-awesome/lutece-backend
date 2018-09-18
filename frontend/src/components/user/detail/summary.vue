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
						<div
							v-show = "all > 0"
							class = "mt-4"
						>
							<Bar
								:data = "data"
								:options = "options"
							/>
						</div>
					</v-flex>
				</v-layout>
			</v-container>
		</v-card>
	</v-hover>
</template>


<script>

import Bar from '@/components/chart/bar';
import JudgeResult from '@/plugins/judge-result';

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
			default: () => ({
				legend: {
					display: false,
				},
				scales: {
					xAxes: [{
						display: false,
						maxBarThickness: 64,
					}],
					yAxes: [{
						display: true,
						ticks: {
							suggestedMin: 0,
							suggestedMax: 6,
						},
					}],
					connectNulls: true,
				},
			}),
		},
	},
	data: () => ({
		data: null,
	}),
	computed: {
		accept() {
			return this.statistics.AC;
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
	created() {
		const label = [];
		const data = [];
		const backgroundColor = [];
		const borderColor = [];
		Object.keys(this.statistics).forEach((key) => {
			const value = this.statistics[key];
			if (Number.isInteger(value) && value > 0) {
				const result = JudgeResult.valueOf[String(key)];
				label.push(JudgeResult.toString[result]);
				data.push(value);
				backgroundColor.push(JudgeResult.backgroundColor[result]);
				borderColor.push(JudgeResult.borderColor[result]);
			}
		});
		const index = [];
		for (let i = 0; i < label.length; i += 1) {
			index.push(i);
		}
		index.sort((i, j) => (
			data[i] < data[j] || (data[i] === data[j] && i > j)
		));
		const mLabel = [];
		const mData = [];
		const mBackgroundColor = [];
		const mBorderColor = [];
		Object.keys(index).forEach((key) => {
			mLabel.push(label[index[key]]);
			mData.push(data[index[key]]);
			mBackgroundColor.push(backgroundColor[index[key]]);
			mBorderColor.push(borderColor[index[key]]);
		});
		this.data = {
			labels: mLabel,
			datasets: [{
				label: 'Statistics',
				backgroundColor: mBackgroundColor,
				borderColor: mBorderColor,
				borderWidth: 1.2,
				data: mData,
			}],
		};
	},
	methods: {
		successRatio(ac, all) {
			if (all === 0) return 0.0;
			return ((100.0 * ac) / all).toFixed(1);
		},
	},
};
</script>
