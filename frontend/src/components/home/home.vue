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
						class = "display-3 lutece"
						style = "text-align:center"
					>
						Lutece
					</h1>
					<div class = "subheading mt-3">
						Lutece是一个基于GNU General Public License Version 3协议开源的Online Judge.
					</div>
					<v-divider class = "my-3"/>
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
			</v-flex>
			<v-container grid-list-xl>
				<v-layout
					row
					wrap
				>
					<v-flex
						v-for = "( each , index ) in cards"
						:key = "index"
						class = "full-height-flex"
						xs12
						md4
					>
						<v-hover>
							<v-card
								slot-scope = "{ hover }"
								:class = "`elevation-${hover ? 4 : 1}`"
								class = "full-height-card">
								<div class = "text-xs-center mt-4">
									<v-icon
										x-large
										class = "blue--text text--lighten-2"> {{ each.icon }} </v-icon>
								</div>
								<div
									primary-title
									class = "layout justify-center mt-4"
								>
									<div class = "headline text-xs-center"> {{ each.title }} </div>
								</div>
								<v-card-text class = "text-xs-center" >
									{{ each.text }}
								</v-card-text>
							</v-card>
						</v-hover>
					</v-flex>
				</v-layout>
			</v-container>
		</v-layout>
	</v-container>
</template>

<script>
export default {
	metaInfo() { return { title: 'Home' }; },
	data: () => ({
		cards: [
			{
				icon: 'mdi-material-design',
				title: 'Material Design',
				text: 'Design based on Google Material, easily to touch beautify',
			},
			{
				icon: 'mdi-flash',
				title: 'Fast and flexible',
				text: 'Core drived by distributed judge Osiris, so powerful and amazing',
			},
			{
				icon: 'mdi-wrench',
				title: 'Easily expandable',
				text: 'Construced by Python and Vue, stand on the shoulders of giants, to build your own Lutece',
			},
		],
		cardHeight: 225,
	}),
};
</script>
