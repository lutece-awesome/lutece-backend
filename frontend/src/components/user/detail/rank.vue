<template>
	<v-hover
		:class = "{
			'pt-4': $vuetify.breakpoint.xsOnly,
			'pb-4': $vuetify.breakpoint.xsOnly
		}"
	>
		<v-card
			slot-scope = "{ hover }"
			:class = "`elevation-${hover ? 4 : 1}`"
			class = "text-xs-center full"
		>
			<v-layout
				align-center
				justify-center
				ma-0
				class = "full"
			>
				<div style = "width:80%" >
					<strong class = "display-1">
						<span> RANK - </span>
						<span> {{ rank }} </span>
					</strong>
					<v-divider class = "mt-4 mb-4" />
					<v-layout
						justify-center
						class = "mt-2"
					>
						<v-flex xs4>
							<div class = "subheading" > SOLVE </div>
							<div class = "title mt-2 success--text" > {{ solved }} </div>
						</v-flex>
						<v-flex xs4>
							<v-divider vertical />
						</v-flex>
						<v-flex xs4>
							<div class = "subheading" > TRY </div>
							<div class = "title mt-2 error--text" > {{ tried }} </div>
						</v-flex>
					</v-layout>
					<v-layout
						justify-center
						class = "mt-5"
					>
						<img
							:src = "require('@/assets/github-dark.svg')"
							height = "35"
						>
						<img
							:src = "require('@/assets/zhihu.svg')"
							height = "35"
							class = "ml-3"
						>
						<img
							:src = "require('@/assets/weibo-dark.svg')"
							height = "35"
							class = "ml-3"
						>
						<img
							:src = "require('@/assets/linkedin-dark.svg')"
							height = "32"
							class = "ml-3"
						>
					</v-layout>
				</div>
			</v-layout>
		</v-card>
	</v-hover>
</template>


<script>
export default {
	props: {
		rank: {
			type: Number,
			default: 0,
		},
		solved: {
			type: Number,
			default: 0,
		},
		tried: {
			type: Number,
			default: 0,
		},
	},
};
</script>

<style scoped>
    .full{
        height: 100%;
        width: 100%;
    }
</style>
