<template>

	<v-layout
		row
		justify-center>
		<v-flex
			xs12
			md8>
			<v-card>
				<v-card-title primary-title>
					<h3 class="headline mb-0">{{ result }}</h3>
				</v-card-title>
				<v-progress-linear
					v-model="progress"
					height="2"
					class="ma-0"/>
				<table class="submission-table output-code mt-2">
					<tr>
						<td><pre>Problem:</pre></td>
						<td>
							<router-link :to="{name: 'ProblemDetailDescription', params: {slug: problem__slug}}">
								<pre>{{ problem__title }}</pre>
							</router-link>
						</td>
					</tr>
					<tr>
						<td><pre>User:</pre></td>
						<td>
							<!-- TODO: User link -->
							<router-link :to="{name: 'ProblemDetailDescription', params: {slug: problem__slug}}">
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
								<td class="text-xs-center">{{ props.item.memory_cost }} MiB</td>
							</tr>
						</template>
					</v-data-table>
				</div>
			</v-card>
		</v-flex>
	</v-layout>

</template>


<script>
import { getWebSocketUri } from '@/utils';

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
		problem__title: null,
		problem__slug: null,
		user__display_name: null,
		user__username: null,
		submit_time: null,
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
	},

	watch: {
		codehighlight(val) {
			this.cmOptions.mode = val;
		},
	},

	beforeRouteLeave(to, from, next) {
		this.ws.close();
		next();
	},

	mounted() {
		this.pk = this.$route.params.pk;
		this.ws = new WebSocket(`${getWebSocketUri()}/status/${String(this.pk)}/?${localStorage.getItem('USER_TOKEN') || ''}`);
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
