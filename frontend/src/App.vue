<template>
	<v-app>
		<Navbar/>
		<v-content>
			<div class = "maincontent" >
				<v-fade-transition
					:duration="100"
					mode="out-in">
					<keep-alive
						v-if="!isAuthenticated || isProfileLoaded"
						include="Problem,Status,User,Blog">
						<router-view/>
					</keep-alive>
				</v-fade-transition>
			</div>
			<Footer/>
		</v-content>
		<Snackbar/>
	</v-app>
</template>

<script>
import Vue from 'vue';
import Footer from '@/components/global/footer';
import Navbar from '@/components/global/navbar';
import Snackbar from '@/components/global/snackbar';
import { mapGetters } from 'vuex';


export default {
	components: {
		Navbar,
		Footer,
		Snackbar,
	},
	computed: {
		...mapGetters({
			isAuthenticated: 'user/isAuthenticated',
			isProfileLoaded: 'user/isProfileLoaded',
		}),
	},
	metaInfo() {
		return {
			title: this.$root.title || 'Lutece',
			titleTemplate: '%s | Lutece',
			meta: [
				{ name: 'theme-color', content: Vue.prototype.$vuetify.theme.primary },
			],
		};
	},
};
</script>

<style scoped>
	.maincontent{
		min-height: 85%;
	}
</style>

