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
					<v-card-title> {{ result }} </v-card-title>
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

	beforeDestory() {
		alert('123');
		this.ws.close();
	},

	mounted() {
		this.pk = this.$route.params.pk;
		this.ws = new WebSocket(`ws://127.0.0.1:8000/ws/status/${String(this.pk)}/`);
		// this.ws.onmessage = function (e) {
		// 	const data = JSON.parse(e.data);
		// 	console.log(data);
		// };
		// this.ws.send('ready');
	},
};
</script>
