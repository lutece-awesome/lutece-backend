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
				<v-card v-if="result">
					<v-card-title primary-title>
						<h3
							:class="result_color + '--text'"
							class="headline mb-0">{{ result }}</h3>
					</v-card-title>
					<v-progress-linear
						:indeterminate="!completed && judge.length == 0"
						v-model="progress"
						:color="result_color"
						height="2"
						class="ma-0"/>
					<table class="submission-table output-code mt-2">
						<tr>
							<td><pre>Problem:</pre></td>
							<td>
								<router-link
									:to="{name: 'ProblemDetailDescription',
										params: {slug: problem__slug}}">
									<pre>{{ problem__title }}</pre>
								</router-link>
							</td>
						</tr>
						<tr>
							<td><pre>User:</pre></td>
							<td>
								<router-link :to="{name: 'UserDetail', params: {username: user__username}}">
									<pre>{{ user__display_name }}</pre>
								</router-link>
							</td>
						</tr>
						<tr>
							<td><pre>Time:</pre></td>
							<td><pre>{{ submit_time }}</pre></td>
						</tr>
					</table>
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
					<div class="py-1"/>
					<div v-if="judge.length > 0">
						<v-divider/>
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
					</div>
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
			return this.judge.length / this.casenumber * 100;
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
