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
						<v-divider class = "mt-2 mb-2" />
					</v-flex>
					<v-flex xs12>
						<table class="summary-table">
							<tr>
								<td>
									<v-icon class = "mdi-18px" >mdi-chart-line </v-icon>
									<span class = "ml-1" > Rank </span>
								</td>
								<td>
									<div class = "green--text text--lighten-2 summaryfont">
										<span> {{ user.rank }} </span>
										<span class = "separate" > / </span>
										<span> {{ user.userall }} </span>
									</div>
								</td>
							</tr>

							<tr>
								<td>
									<v-icon class = "mdi-18px" >mdi-lightbulb-on-outline </v-icon>
									<span class = "ml-1" > Problem </span>
								</td>
								<td>
									<div class = "light-blue--text text--lighten-2 summaryfont">
										<span> {{ user.solved }} </span>
										<span class = "separate" > / </span>
										<span> {{ user.tried }} </span>
									</div>
								</td>
							</tr>

							<tr>
								<td>
									<v-icon class = "mdi-18px" >mdi-poll</v-icon>
									<span class = "ml-1" > Submissions </span>
								</td>
								<td>
									<div class = "orange--text summaryfont text--lighten-2">
										<span> {{ accept }} </span>
										<span class = "separate" > / </span>
										<span> {{ all }} </span>
									</div>
								</td>
							</tr>

							<tr>
								<td>
									<v-icon class = "mdi-18px" >mdi-check </v-icon>
									<span class = "ml-1" > Ratio </span>
								</td>
								<td >
									<div class = "indigo--text text--lighten-2 summaryfont">
										<span> {{ successRatio( accept , all ) }} % </span>
									</div>
								</td>
							</tr>

						</table>

						<div
							v-show = "all > 0"
							class = "mt-4"
						>
							<Bar
								:data = "data"
								:options = "options"
								style = "height: 300px"
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
		user: {
			type: Object,
			default: null,
		},
		options: {
			type: Object,
			default: () => ({
				legend: {
					display: false,
				},
				maintainAspectRatio: false,
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
		statistics: null,
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
		this.statistics = this.user.submissionStatistics;
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

<style scoped>
	.summaryfont{
		font-weight: 600;
	}
	.separate{
		margin-left: 2px;
		margin-right: 2px;
	}
</style>
