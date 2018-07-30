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
					<span class="subheading">Lorem ipsum dolor sit amet, pri veniam forensibus id.
					Vis maluisset molestiae id, ad semper lobortis cum. At impetus detraxit incorru
					pte usu, repudiare assueverit ex eum, ne
					nam essent vocent admodum.
					</span>
					<v-divider class="my-3"/>
					<div class="title mb-3">Star Lutece on GITHUB!</div>
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
					</v-btn>
				</div>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
export default {
	metaInfo() { return { title: 'Home' }; },
};
</script>
