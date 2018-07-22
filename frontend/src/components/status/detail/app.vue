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
export default {
	data: () => ({
		pk: '',
		code: '',
		result: '',
		judge: [],
		ws: null,
	}),

	beforeRouteLeave(to, from, next) {
		this.ws.close();
		next();
	},

	mounted() {
		this.pk = this.$route.params.pk;
		this.ws = new WebSocket(`${`ws://127.0.0.1:8000/ws/status/${String(this.pk)}/` + '?'}${localStorage.getItem('USER_TOKEN')}` || '');
		this.ws.onmessage = (event) => {
			let { data } = event;
			data = JSON.parse(data);
			this.judge = data.judge;
			this.result = data.result;
		};
	},
};
</script>
