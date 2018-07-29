<template>
	<v-app>
		<Navbar/>
		<v-content>
			<keep-alive include="Problem,Status,User">
				<v-slide-y-transition mode="out-in">
					<router-view/>
				</v-slide-y-transition>
			</keep-alive>
		</v-content>
		<Snackbar/>
	</v-app>
</template>

<script>
import Vue from 'vue';
import Footer from '@/components/global/footer';
import Navbar from '@/components/global/navbar';
import Snackbar from '@/components/global/snackbar';

export default {
	components: {
		Navbar,
		Footer,
		Snackbar,
	},
	metaInfo() {
		return {
			title: 'Lutece',
			titleTemplate: '%s | Lutece',
			meta: [
				{ name: 'theme-color', content: Vue.prototype.$vuetify.theme.primary },
			],
		};
	},
};
</script>

<style>
span.mord {
	background-color: transparent !important;
    border-color: transparent !important;
}
</style>
