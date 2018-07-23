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
					class="mt-1"/>
				<codemirror
					v-model="code"
					:options="cmOptions"
				/>
				<v-card-text v-if="judgererror_msg">
					<pre>{{ judgererror_msg }}</pre>
				</v-card-text>
				<v-card-text v-if="compileerror_msg">
					<pre>{{ compileerror_msg }}</pre>
				</v-card-text>
				<v-divider class="mt-3"/>
				<v-data-table
					v-if="judge.length > 0"
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
		code: '',
		compileerror_msg: '',
		judgererror_msg: '',
		result: '',
		casenumber: 0,
		judge: [],
		ws: null,
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
			for (let i = 0; i < data.judge.length; i += 1) { this.judge.push(data.judge[i]); }
			if (Object.prototype.hasOwnProperty.call(data, 'result')) { this.result = data.result; }
			if (Object.prototype.hasOwnProperty.call(data, 'casenumber')) { this.casenumber = data.casenumber; }
			if (Object.prototype.hasOwnProperty.call(data, 'code')) { this.code = data.code; }
			if (Object.prototype.hasOwnProperty.call(data, 'codehighlight')) { this.cmOptions.mode = data.codehighlight; }
			if (Object.prototype.hasOwnProperty.call(data, 'compileerror_msg')) { this.compileerror_msg = data.compileerror_msg; }
			if (Object.prototype.hasOwnProperty.call(data, 'judgererror_msg')) { this.judgererror_msg = data.judgererror_msg; }
		};
	},
};
</script>
