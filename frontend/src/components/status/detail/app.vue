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
				<v-card
					v-if = "result"
					hover
					style = "cursor:default"
				>
					<v-card-title primary-title>
						<h3
							:class = "result_color + '--text'"
							class = "headline mb-0">
							{{ result }}
						</h3>
					</v-card-title>
					<v-progress-linear
						:indeterminate="!completed && judge.length == 0"
						v-model="progress"
						:color="result_color"
						height="2"
						class="ma-0"/>
					<v-card-text>
						<table class="submission-table output-code mt-2">
							<tr>
								<td><pre>Problem:</pre></td>
								<td class = "pl-1">
									<router-link
										:to="{name: 'ProblemDetailDescription',
											params: {slug: problem__slug}}"
										tag = "a">
										{{ problem__title }}
									</router-link>
								</td>
							</tr>
							<tr>
								<td><pre>User:</pre></td>
								<td class = "pl-1">
									<router-link :to="{name: 'UserDetail', params: {username: user__username}}">
										{{ user__display_name }}
									</router-link>
								</td>
							</tr>
							<tr>
								<td><pre>Time:</pre></td>
								<td class = "pl-1"><pre>{{ submit_time }}</pre></td>
							</tr>
							<tr>
								<td><pre>Case:</pre></td>
								<td
									class = "pl-1" >
									<span :class = "result_color + '--text'">
										{{ judge.length }} / {{ casenumber }}
									</span>
								</td>
						</tr></table>
					</v-card-text>
				</v-card>
				<v-card
					hover
					class = "mt-5"
					style = "cursor:default" >
					<v-tabs
						v-model = "tabs"
						fixed-tabs>
						<v-tab :ripple = "false"> Code </v-tab>
						<v-tab :ripple = "false"> Progress </v-tab>
					</v-tabs>
					<v-tabs-items
						v-model = "tabs"
						touchless
					>
						<v-tab-item id = "Code">
							<v-card>
								<v-card-text>
									<codemirror
										v-if="code"
										v-model="code"
										:options="cmOptions"
									/>
									<div
										v-if="judgererror_msg"
										class="output-code">
										<pre>{{ judgererror_msg }}</pre>
									</div>
									<div
										v-if="compileerror_msg"
										class="output-code">
										<pre>{{ compileerror_msg }}</pre>
									</div>
								</v-card-text>
							</v-card>
						</v-tab-item>
						<v-tab-item id = "Progress">
							<v-card>
								<v-card-text>
									<v-data-table
										:items="judge"
										:headers="headers"
										dense
										hide-actions>
										<template
											slot="items"
											slot-scope="props">
											<tr>
												<td class="text-xs-center">{{ props.item.case }}</td>
												<td class="text-xs-center">{{ props.item.result }}</td>
												<td class="text-xs-center">{{ props.item.time_cost }} ms</td>
												<td class="text-xs-center">{{ props.item.memory_cost }} KiB</td>
											</tr>
										</template>
									</v-data-table>
								</v-card-text>
							</v-card>
						</v-tab-item>
					</v-tabs-items>
				</v-card>
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>
import { getWebSocketUri } from '@/utils';
import { mapGetters } from 'vuex';


export default {
	components: {
		codemirror: () => import('@/components/basic/codemirror'),
	},
	metaInfo() { return { title: `Submission#${this.pk}` }; },
	data: () => ({
		tabs: null,
		pk: '',
		judge: [],
		ws: null,
		result: null,
		compileerror_msg: null,
		judgererror_msg: null,
		code: null,
		casenumber: null,
		codehighlight: null,
		completed: false,
		problem__title: null,
		problem__slug: null,
		user__display_name: null,
		user__username: null,
		submit_time: null,
		result_color: 'info',
		headers: [
			{
				text: 'Case',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Verdict',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Time',
				align: 'center',
				sortable: false,
			},
			{
				text: 'Memory',
				align: 'center',
				sortable: false,
			},
		],
		cmOptions: {
			indentUnit: 4,
			lineNumbers: true,
			matchBrackets: true,
			mode: '',
			theme: 'neo',
			readOnly: true,
		},
	}),

	computed: {
		progress() {
			return (this.judge.length / this.casenumber) * 100;
		},
		...mapGetters({
			token: 'user/token',
		}),
	},

	watch: {
		codehighlight(val) {
			this.cmOptions.mode = val;
		},
		completed(val) {
			if (val) {
				this.ws.close();
			}
		},
	},

	beforeRouteLeave(to, from, next) {
		this.ws.close();
		next();
	},

	mounted() {
		this.pk = this.$route.params.pk;
		this.ws = new WebSocket(`${getWebSocketUri()}/status/${String(this.pk)}/?${this.token}`);
		this.ws.onmessage = (event) => {
			let { data } = event;
			data = JSON.parse(data);
			if (data.judge !== undefined) {
				data.judge = this.judge.concat(data.judge);
			}
			Object.assign(this, data);
		};
	},
};
</script>
