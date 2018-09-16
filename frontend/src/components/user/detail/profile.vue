<template>
	<v-hover>
		<v-card
			slot-scope = "{ hover }"
			:class = "`elevation-${hover ? 4 : 1}`"
			class = "pl-3 pr-3 pt-3 pb-3">
			<v-layout
				row
				wrap>
				<v-flex
					:class = "{'xs12': $vuetify.breakpoint.xsOnly, 'xs5': !$vuetify.breakpoint.xsOnly }"
					text-xs-center>
					<v-layout
						fill-height
						align-center
						justify-center
						ma-0
					>
						<v-img
							:src = "user.gravataremail"
							max-height = "160"
							class = "pl-4 pr-4 pu-4 pb-4"
							contain
						/>
					</v-layout>
				</v-flex>
				<v-flex
					:class = "{'xs12': $vuetify.breakpoint.xsOnly, 'xs7': !$vuetify.breakpoint.xsOnly }"
					class = "pl-4">
					<h3 class = "headline text-xs-center mt-3">
						{{ user.displayName }}
					</h3>
					<v-divider class = "mt-2" />
					<div class = "mt-2" >
						<v-icon class = "mdi-18px">mdi-school</v-icon>
						<span class = "ml-1"> {{ user.school }} </span>
					</div>
					<div class = "mt-2" >
						<v-icon class = "mdi-18px">mdi-domain</v-icon>
						<span class = "ml-1"> {{ user.company }} </span>
					</div>
					<div class = "mt-2" >
						<v-icon class = "mdi-18px">mdi-map-marker</v-icon>
						<span class = "ml-1"> {{ user.location }} </span>
					</div>
					<div class = "mt-2">
						<v-tooltip bottom>
							<span slot = "activator">
								<v-icon class = "mdi-18px">mdi-flag-variant</v-icon>
								<span class = "ml-1" >
									{{ user.lastloginDate | moment("from") }}
								</span>
							</span>
							<span>
								Last visited in
								{{ user.lastloginDate | moment("dddd, MMMM Do YYYY, h:mm:ss a") }}
							</span>
						</v-tooltip>
					</div>
					<div class = "mt-2" >
						<v-tooltip bottom>
							<span slot = "activator">
								<v-icon class = "mdi-18px">mdi-emoticon-cool</v-icon>
								<span class = "ml-1">
									{{ user.joinedDate | moment("from") }}
								</span>
							</span>
							<span>
								Joined in {{ user.lastloginDate | moment( "MMMM Do, YYYY" ) }}
							</span>
						</v-tooltip>
					</div>
				</v-flex>
			</v-layout>
			<v-divider class = "mt-2" />
			<v-card-text>
				<div class = "about">
					{{ user.about }}
				</div>
			</v-card-text>
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

<style scoped>
    .about{
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>
