<template>
	<v-app>
		<Navbar/>
		<v-content>
			<v-container fluid>
				<transition name="fade">
					<router-view/>
				</transition>
			</v-container>
		</v-content>
	</v-app>
</template>

<script>
import Footer from '@/components/global/footer';
import Navbar from '@/components/global/navbar';

export default {
	components: {
		Navbar,
		Footer,
	},
};
</script>

<style>
.v-label.error--text {
	animation: none !important;
}

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
