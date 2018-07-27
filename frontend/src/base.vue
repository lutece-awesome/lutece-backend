<template>
	<v-app>
		<Navbar/>
		<v-content>
			<v-container
				:class="{'pa-0': $vuetify.breakpoint.xsOnly }"
				fluid>
				<transition name="fade">
					<keep-alive>
						<router-view v-if="$route.meta.keepAlive"/>
					</keep-alive>
				</transition>
				<transition name="fade">
					<router-view v-if="!($route.meta.keepAlive || false)"/>
				</transition>
			</v-container>
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
.fade-enter-active, .fade-leave-active {
	transition-property: opacity;
	transition-duration: .1s;
}

.fade-enter-active {
	transition-delay: .1s;
}

.fade-enter, .fade-leave-active {
	opacity: 0
}

span.mord {
	background-color: transparent !important;
    border-color: transparent !important;
}
</style>
