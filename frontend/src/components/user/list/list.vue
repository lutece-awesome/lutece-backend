<template>
	<v-card>
		<v-list subheader>
			<v-subheader>Top Solved</v-subheader>
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
	<!-- <v-container>
		<v-layout
			row
			wrap>
			<v-flex
				v-for = "( each , index ) in userItem "
				:key = "index"
				xs12
				sm4>
				<v-card>
					<v-card-media
						:src = "each.gravataremail"
						height = "200px"
					/>
					<v-card-title primary-title>
						{{ each.displayName }}
					</v-card-title>
				</v-card>
			</v-flex>
		</v-layout>
	</v-container> -->
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
