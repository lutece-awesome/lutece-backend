<template>
	<v-hover>
		<v-card
			slot-scope = "{ hover }"
			:class = "`elevation-${hover ? 4 : 1}`"
		>
			<div>
				<v-container>
					<v-layout
						row
						wrap>
						<v-flex xs12>
							<h3>
								<v-icon class = "mdi-18px"> mdi-chart-gantt </v-icon>
								<span class = "ml-1"> Solved </span>
							</h3>
							<v-divider class = "mt-2 mb-2" />
							<div>
								<v-btn
									v-for = "each in user.analysis"
									:key = "each[0]"
									:to = "{name: 'ProblemDetailDescription', params: {slug: each[2] }}"
									small
									round

									color = " each[1] == 'yes' ? success : error "
								>
									{{ each[0] }}
								</v-btn>
							</div>
						</v-flex>
					</v-layout>
				</v-container>
			</div>
		</v-card>
	</v-hover>
</template>


<script>
export default {
	props: {
		user: {
			type: Object,
			default: null,
		},
	},
};
</script>
