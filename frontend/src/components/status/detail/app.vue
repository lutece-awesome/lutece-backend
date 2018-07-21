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
						Detail
					</v-toolbar-title>
					<v-spacer/>
				</v-toolbar>
			</v-card>
		</v-flex>
	</v-layout>

</template>


<script>
export default {
	data: () => ({
		code: '',
	}),
};
</script>
