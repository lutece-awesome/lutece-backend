<template>
	<div>
		<v-card
			v-for = "( each , index ) in items"
			:key = "index"
			:to = "{name: 'BlogDetail', params: {slug: each.slug }}"
			class = "mb-4"
			hover
			raised
		>
			<v-container>
				<v-layout
					row
					wrap>
					<v-flex xs8>
						<div class = "header" >
							{{ each.title }}
						</div>
					</v-flex>
					<v-flex
						xs4
						text-xs-right
						class = "pt-2 subheader">
						<v-icon small > mdi-library-books </v-icon>
						{{ each.view | thoundNumberic }} views
					</v-flex>
					<v-flex xs12 >
						<v-divider class = "mt-3 mb-3" />
					</v-flex>
					<v-flex xs12>
						<div class = "subheader">
							<span>
								<v-avatar
									size = "40"
								>
									<img :src = "each.user.gravataremail" >
								</v-avatar>
								<span class = "ml-2" > <a> {{ each.user.displayName }} </a> </span>
							</span>
							<span
								style = "float:right"
								class = "pt-2" >
								<span>
									<v-icon small> mdi-star </v-icon>
									{{ each.vote | thoundNumberic }} stars
								</span>
								<span class = "ml-1 mr-1" > | </span>
								<span> {{ each.createTime | moment("MMMM Do, YYYY") }} </span>
							</span>
						</div>
					</v-flex>
				</v-layout>
			</v-container>
		</v-card>
	</div>
</template>


<script>

import { getThoundNumberic } from '@/utils';

export default {

	filters: {
		thoundNumberic: getThoundNumberic,
	},
	props: {
		items: {
			type: Array,
			default: () => [],
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
</style>
