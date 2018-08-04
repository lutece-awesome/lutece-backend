<!--
    Homepage
-->
<template>
	<v-container fluid>
		<v-layout
			row
			justify-center
			wrap>
			<v-flex
				xs12
				sm8>
				<div>
					<h1
						class="display-3"
						style = "text-align:center;" >Lutece </h1>
					<span class="subheading">Lutece是一个基于GNU General Public License Version 3协议开源的Online Judge.
					</span>
					<v-divider class="my-3"/>
					<!-- <div class="title mb-3">Star Lutece on GITHUB!</div>
					<v-btn
						class="mx-0"
						color="primary"
						large
						href="https://github.com/LaPluses/Lutece"
					>
						<v-icon
							left
							dark>mdi-github-circle</v-icon>
						Github
					</v-btn> -->
				</div>
				<section>
					<v-layout
						column
						wrap
						class="my-5"
						align-center
					>
						<v-flex
							xs12
							sm4
							class="my-3"/>
						<v-flex xs12>
							<v-container grid-list-xl>
								<v-layout
									row
									wrap
									align-center>
									<v-flex
										xs12
										md4>
										<v-card class="elevation-0 transparent">
											<v-card-text class="text-xs-center">
												<v-icon
													x-large
													class="blue--text text--lighten-2">mdi-emoticon-cool</v-icon>
											</v-card-text>
											<v-card-title
												primary-title
												class="layout justify-center">
												<div class="headline text-xs-center">Material Design</div>
											</v-card-title>
											<v-card-text>
												基于遵守Google Material设计范式的Vuetify UI Framework打造,无论是通过PC,平板,手机,都能拥有最完美的体验,
												同时深度优化的SPA带来如丝般顺滑的游览体验.
											</v-card-text>
										</v-card>
									</v-flex>
									<v-flex
										xs12
										md4>
										<v-card class="elevation-0 transparent">
											<v-card-text class="text-xs-center">
												<v-icon
													x-large
													class="blue--text text--lighten-2">mdi-flash</v-icon>
											</v-card-text>
											<v-card-title
												primary-title
												class="layout justify-center">
												<div class="headline">Fast and flexible</div>
											</v-card-title>
											<v-card-text>
												借助于分布式的Osiris(奥西里斯)内核,可灵活的将判题任务分布至多台机器上,即使是最为基础的学生云服务器,也能轻松支撑数百人的比赛.
											</v-card-text>
										</v-card>
									</v-flex>
									<v-flex
										xs12
										md4>
										<v-card class="elevation-0 transparent">
											<v-card-text class="text-xs-center">
												<v-icon
													x-large
													class="blue--text text--lighten-2">mdi-wrench</v-icon>
											</v-card-text>
											<v-card-title
												primary-title
												class="layout justify-center">
												<div class="headline text-xs-center">Easily expandable</div>
											</v-card-title>
											<v-card-text>
												Lutece基于Python的Django框架实现,借助于Python的海量第三方库,站在巨人的肩膀上实现任意的功能拓展,打造属于你自己的Lutece.
											</v-card-text>
										</v-card>
									</v-flex>
								</v-layout>
							</v-container>
						</v-flex>
					</v-layout>
				</section>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
export default {
	metaInfo() { return { title: 'Home' }; },
};
</script>
