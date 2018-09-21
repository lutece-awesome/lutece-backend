<template>
	<div>
		<v-layout
			row
			wrap>
			<v-flex xs12>
				<v-img
					:src = "user.gravataremail"
					height = "200"
					contain
				>
					<LoadingSpinner slot = "placeholder" />
				</v-img>
			</v-flex>
			<v-flex
				xs12
				class = "mt-3" >
				<v-hover>
					<v-card
						slot-scope = "{ hover }"
						:class = "`elevation-${hover ? 4 : 1}`"
					>
						<v-container>
							<v-layout
								row
								wrap>
								<v-flex xs12>
									<div class = "headline font-weight-medium ml-1" > {{ user.displayName }} </div>
									<v-divider class = "mt-2 mb-2" />
									<table class="profile-table">
										<tr>
											<td>Last Seen</td>
											<td>
												<v-tooltip bottom>
													<span slot = "activator">
														<span>
															{{ user.lastloginDate | moment("from") }}
														</span>
													</span>
													<span>
														{{ user.lastloginDate | moment("dddd, MMMM Do YYYY, h:mm:ss a") }}
													</span>
												</v-tooltip>
											</td>
										</tr>
										<tr>
											<td>Registered</td>
											<td>
												<v-tooltip bottom>
													<span slot = "activator">
														<span>
															{{ user.joinedDate | moment("from") }}
														</span>
													</span>
													<span>
														{{ user.lastloginDate | moment( "MMMM Do, YYYY" ) }}
													</span>
												</v-tooltip>
											</td>
										</tr>
										<tr v-if = "user.school" >
											<td>School</td>
											<td>{{ user.school }}</td>
										</tr>
										<tr v-if = "user.company" >
											<td>Company</td>
											<td>{{ user.company }}</td>
										</tr>
										<tr v-if = "user.location" >
											<td>Location</td>
											<td>{{ user.location }}</td>
										</tr>
										<tr v-if = "user.about">
											<td>Society</td>
											<td>
												<img
													:src = "require('@/assets/github.svg')"
													height = "24"
												>
												<img
													:src = "require('@/assets/zhihu.svg')"
													height = "24"
													class = "ml-2"
												>
												<img
													:src = "require('@/assets/weibo.svg')"
													height = "24"
													class = "ml-2"
												>
												<img
													:src = "require('@/assets/linkedin.svg')"
													height = "24"
													class = "ml-2"
												>
											</td>
										</tr>
										<tr v-if = "user.about">
											<td>About</td>
											<td>{{ user.about }}</td>
										</tr>
									</table>
								</v-flex>
							</v-layout>
						</v-container>
					</v-card>
				</v-hover>
			</v-flex>
		</v-layout>
	</div>
</template>


<script>

import LoadingSpinner from '@/components/basic/loadingspinner';

export default {

	components: {
		LoadingSpinner,
	},

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
