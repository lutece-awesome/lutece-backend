<template>
	<v-container fluid>
		<v-layout
			row
			justify-center>
			<v-flex
				v-show = "result"
				xs12
				md8>
				<v-hover>
					<v-card
						slot-scope = "{ hover }"
						:class = "`elevation-${hover ? 4 : 1}`"
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
											:to = "{name: 'ProblemDetailDescription',
												params: {slug: problem__slug}}"
											tag = "a"
										>
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
				</v-hover>

				<v-hover>
					<v-card
						slot-scope = "{ hover }"
						:class = "`elevation-${hover ? 4 : 1}`"
						class = "mt-5"
					>

						<div v-if = "hasCode">
							<v-tabs
								v-model = "tabs"
								fixed-tabs>
								<v-tab :ripple = "false"> Code </v-tab>
								<v-tab :ripple = "false"> Progress </v-tab>
							</v-tabs>
						</div>
						<div v-else>
							<v-tabs
								v-model = "tabs"
								fixed-tabs>
								<v-tab :ripple = "false"> Progress </v-tab>
							</v-tabs>
						</div>

						<div v-if = "hasCode">
							<v-tabs-items
								v-model = "tabs"
								touchless
							>

								<v-tab-item>
									<codeComponent
										:code = "code"
										:judgererror_msg = "judgererror_msg"
										:compileerror_msg = "compileerror_msg"
										:cm-options = "cmOptions"
									/>
								</v-tab-item>

								<v-tab-item>
									<progressComponent
										:judge = "judge"
										:headers = "headers" />
								</v-tab-item>

							</v-tabs-items>
						</div>
						<div v-else>
							<v-tabs-items
								v-model = "tabs"
								touchless
							>
								<v-tab-item>
									<progressComponent
										:judge = "judge"
										:headers = "headers" />
								</v-tab-item>

							</v-tabs-items>
						</div>
					</v-card>
				</v-hover>
			</v-flex>
		</v-layout>
	</v-container>
</template>


<script>
import { getWebSocketUri } from '@/utils';
import { mapGetters } from 'vuex';


export default {
	components: {
		codeComponent: () => import('@/components/status/detail/code'),
		progressComponent: () => import('@/components/status/detail/progress'),
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
		cmOptions: {
			indentUnit: 4,
			lineNumbers: true,
			matchBrackets: true,
			mode: '',
			theme: 'neo',
			readOnly: true,
		},
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

	}),

	computed: {
		progress() {
			return (this.judge.length / this.casenumber) * 100;
		},
		...mapGetters({
			token: 'user/token',
		}),
		hasCode() {
			if (!this.code) return false;
			return this.code.length > 0;
		},
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
