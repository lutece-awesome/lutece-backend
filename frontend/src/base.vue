<template>
	<v-app>
		<Navbar/>
		<v-content>
			<keep-alive include="Problem,Status,User">
				<transition
					name="component-fade"
					mode="out-in">
					<router-view/>
				</transition>
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
.component-fade-enter-active, .component-fade-leave-active {
	transition: opacity .1s ease;
}

.component-fade-enter, .component-fade-leave-to {
	opacity: 0;
}

span.mord {
	background-color: transparent !important;
    border-color: transparent !important;
}
</style>
