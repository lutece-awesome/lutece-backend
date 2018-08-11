<template>
	<div>
		<v-card class = "card" >
			<v-container>
				<v-layout
					row
					wrap>
					<v-flex xs8>
						<div class = "header" >
							You can change the world and make it better
						</div>
					</v-flex>
					<v-flex
						xs4
						text-xs-right
						class = "pt-2 subheader">
						<v-icon small > mdi-library-books </v-icon>
						20k views
					</v-flex>
					<v-flex xs12>
						<v-divider class = "mt-3 mb-3" />
						<div class = "subheader">
							<span>
								<v-avatar
									size = "40"
								>
									<img src = "https://secure.gravatar.com/avatar/79bc21937a1f625d1cf08c919f8c70c2.jpg?r=g&s=300&d=mm">
								</v-avatar>
								<span> <a> Inventure </a> </span>
							</span>
							<span
								style = "float:right"
								class = "pt-2" >
								<span>
									<v-icon small> mdi-star </v-icon>
									0 stars
								</span>
								<span class = "ml-1 mr-1" > | </span>
								<span> July, 30th, 2020 </span>
							</span>
						</div>
					</v-flex>
					<!-- <v-flex
						xs6
						text-xs-left>
						<div>
							<v-avatar
								size = "36"
								class = "mr-2"
							>
								<img src = "https://secure.gravatar.com/avatar/79bc219….jpg?r=g&d=mm&s=250">
							</v-avatar>
							<a>123</a>
						</div>
					</v-flex>
					<v-flex
						xs6
						text-xs-right>
						<div>
							<v-avatar
								size = "36"
								class = "mr-2"
							/>
							July, 18, 2018
						</div>
					</v-flex> -->
				</v-layout>
			</v-container>
		</v-card>
	</div>
</template>


<script>
export default {
	props: {
		items: {
			type: Array,
			default: () => [],
		},
		isLoading: {
			type: Boolean,
			default: false,
		},
	},
};
</script>

<style scoped>
	.header {
		font-size: 18px;
		font-weight: 400;
	}

	.subheader {
		font-size: 14px;
		font-weight: 400;
		color: grey;
	}

	.view {
		background: #eee;
		border: 1px solid #f0f0f0;
		line-height: 20px;
		font-size: 14px;
		font-family: 'Monaco', courier, monospace;
		padding: 10px;
	}

	.card:hover{
		box-shadow: 2px 2px 2px #888888;
	}
</style>
