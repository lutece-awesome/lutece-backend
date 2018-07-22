<template>

	<v-layout
		row
		justify-center>
		<v-flex
			xs12
			md8>
			<v-card>
				<v-toolbar
					card
					prominent>
					<v-toolbar-title>
						JudgeStatus
					</v-toolbar-title>
					<v-spacer/>
				</v-toolbar>
				<v-card>
					<v-card-title primary-title>
						<div>
							<h3 class="headline mb-0">{{ result }}</h3>
						</div>
					</v-card-title>
					<v-card-text>
						<v-btn
							v-for = "(each , index ) in judge"
							:key = "each.index" > {{ each.result }} </v-btn>
					</v-card-text>
				</v-card>
			</v-card>
		</v-flex>
	</v-layout>

</template>


<script>
import { getWebSocketUri } from '@/utils';

export default {
	data: () => ({
		pk: '',
		code: '',
		codehighlight: '',
		compileerror_msg: '',
		judgererror_msg: '',
		result: '',
		casenumber: 0,
		judge: [],
		ws: null,
	}),

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
			if (Object.prototype.hasOwnProperty.call(data, 'code')) { this.casenumber = data.code; }
			if (Object.prototype.hasOwnProperty.call(data, 'codehighlight')) { this.casenumber = data.codehighlight; }
			if (Object.prototype.hasOwnProperty.call(data, 'compileerror_msg')) { this.compileerror_msg = data.compileerror_msg; }
			if (Object.prototype.hasOwnProperty.call(data, 'judgererror_msg')) { this.casenumber = data.judgererror_msg; }
		};
	},
};
</script>
