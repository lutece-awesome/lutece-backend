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
import { getWebSocketUri } from '@/utils';

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
		this.ws = new WebSocket(`${getWebSocketUri()}/status/${String(this.pk)}/`);
	},
};
</script>
