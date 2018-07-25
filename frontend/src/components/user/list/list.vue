<template>
	<v-card>
		<v-list two-line>
			<v-list-tile
				v-for = "each in userItem"
				:key = "each.displayName"
				avatar
			>
				<v-list-tile-avatar>
					<img :src = "each.gravataremail" >
				</v-list-tile-avatar>
				<v-list-tile-content>
					<v-list-tile-title> {{ each.displayName }} </v-list-tile-title>
				</v-list-tile-content>

				<v-list-tile-action>
					<v-icon :color = "teal" > mdi-login </v-icon>
				</v-list-tile-action>

			</v-list-tile>
		</v-list>
	</v-card>
</template>


<script>
export default {
	props: {
		userItem: {
			type: Array,
			default: () => [],
		},
	},
};
</script>
