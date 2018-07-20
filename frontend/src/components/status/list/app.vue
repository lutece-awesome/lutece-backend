<template>

	<v-layout
		row
		justify-center>
		<v-flex
			v-if = "!isLoading"
			xs12
			md8>
			<v-card>
				<v-toolbar
					card
					prominent>
					<v-toolbar-title>
						Status
					</v-toolbar-title>
					<v-spacer/>
				</v-toolbar>
				<StatusList :status-item = "statusItem" />
			</v-card>
			<div class="text-xs-center mt-2">
				<v-pagination
					v-model="page"
					:length="maxpage"/>
			</div>
		</v-flex>
	</v-layout>

</template>


<script>

import StatusList from '@/components/status/list/list';


export default {

	components: {
		StatusList,
	},

	data() {
		return {
			isLoading: false,
			page: 0,
			maxpage: 0,
			statusItem: [],
		};
	},
};
</script>
