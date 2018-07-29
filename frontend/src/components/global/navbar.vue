<template>
	<div>
		<v-navigation-drawer
			v-model="drawer"
			:width="240"
			:mini-variant="$vuetify.breakpoint.mdOnly"
			fixed
			clipped
			mobile-break-point="960"
			app>
			<v-toolbar
				flat
				class="hidden-sm-and-up">
				<v-list-tile >
					<v-list-tile-content>
						<v-list-tile-title class="title">Lutece</v-list-tile-title>
					</v-list-tile-content>
				</v-list-tile>
			</v-toolbar>
			<v-divider class="hidden-sm-and-up"/>
			<v-list>
				<v-list-tile
					v-for="item in items"
					:key="item.title"
					:to="item.path"
					ripple
					active-class="grey lighten-3">
					<v-list-tile-action>
						<v-icon>{{ item.icon }}</v-icon>
					</v-list-tile-action>
					<v-list-tile-content>
						<v-list-tile-title>{{ item.title }}</v-list-tile-title>
					</v-list-tile-content>
				</v-list-tile>
			</v-list>
		</v-navigation-drawer>
		<v-toolbar
			fixed
			clipped-left
			app
			dark
			color="primary">
			<v-toolbar-side-icon @click.stop="drawer=!drawer"/>
			<v-toolbar-title class="hidden-xs-only">
				Lutece
			</v-toolbar-title>
			<v-divider
				class="mx-3 hidden-xs-only"
				inset
				vertical
			/>
			<span class="subheading hidden-xs-only">{{ title }}</span>
			<v-toolbar-title class="hidden-sm-and-up">{{ title }}</v-toolbar-title>
			<v-spacer/>
			<v-toolbar-items class="hidden-sm-and-down">
				<v-btn
					v-if="!isAuthenticated"
					:to="login"
					flat>
					<v-icon class="mr-2">mdi-login</v-icon>
					SIGN IN
				</v-btn>
				<v-menu
					v-if="isProfileLoaded"
					open-on-hover
					offset-y>
					<v-btn
						slot="activator"
						flat>
						<v-avatar
							size="36"
							class="mr-2" >
							<img :src="profile.gravataremail" >
						</v-avatar>
						{{ profile.	displayName }}
						<v-icon>mdi-menu-down</v-icon>
					</v-btn>
					<v-list>
						<v-list-tile
							v-for="item in dropdownItems"
							:key="item.label"
							:to="item.route"
							active-class="grey lighten-3">
							<v-icon class="mr-2">{{ item.icon }}</v-icon>
							<v-list-tile-content>
								<v-list-tile-title>{{ item.label }}</v-list-tile-title>
							</v-list-tile-content>
						</v-list-tile>
					</v-list>
				</v-menu>
			</v-toolbar-items>
			<v-btn
				v-if="isProfileLoaded"
				:to="userDetail"
				icon
				class="hidden-md-and-up">
				<v-avatar size="36">
					<img :src="profile.gravataremail" >
				</v-avatar>
			</v-btn>
			<v-btn
				v-if="isProfileLoaded"
				:to="signOut"
				icon
				class="hidden-md-and-up">
				<v-icon>mdi-logout</v-icon>
			</v-btn>
			<v-btn
				v-if="!isAuthenticated"
				:to="login"
				icon
				class="hidden-md-and-up">
				<v-icon>mdi-login</v-icon>
			</v-btn>
		</v-toolbar>
	</div>
</template>

<script>
import { mapGetters } from 'vuex';
import Login from '@/components/signin/login';

export default {
	components: {
		Login,
	},
	data() {
		return {
			drawer: null,
			signin: false,
			items: [
				{
					icon: 'mdi-home',
					title: 'Home',
					path: '/home',
				},
				{
					icon: 'mdi-view-list',
					title: 'Problem',
					path: '/problem',
				},
				{
					icon: 'mdi-chart-bar',
					title: 'Status',
					path: '/status',
				},
				{
					icon: 'mdi-trophy',
					title: 'Contest',
					path: '/contest',
				},
				{
					icon: 'mdi-account-multiple',
					title: 'User',
					path: '/user',
				},
				{
					icon: 'mdi-book-open',
					title: 'Blog',
					path: '/blog',
				},
				{
					icon: 'mdi-information',
					title: 'About',
					path: '/about',
				},
			],
		};
	},
	computed: {
		...mapGetters({
			profile: 'user/profile',
			payload: 'user/payload',
			isAuthenticated: 'user/isAuthenticated',
			isProfileLoaded: 'user/isProfileLoaded',
		}),
		title() {
			return this.$root.title;
		},
		login() {
			return {
				name: 'Login',
				query: {
					redirect: this.$route.query.redirect || this.$route.path,
				},
			};
		},
		userDetail() {
			return {
				name: 'UserDetail',
				params: { username: this.payload.username },
			};
		},
		userSettings() {
			return { name: 'UserSettings' };
		},
		signOut() {
			return {
				name: 'Signout',
				query: {
					redirect: this.$route.path,
				},
			};
		},
		dropdownItems() {
			return [
				{
					route: this.userDetail,
					icon: 'mdi-account',
					label: 'Profile',
				},
				{
					route: this.userSettings,
					icon: 'mdi-settings',
					label: 'Settings',
				},
				{
					route: this.signOut,
					icon: 'mdi-logout',
					label: 'Sign Out',
				},
			];
		},
	},
	metaInfo: {
		changed(newInfo, _addedTags, _removedTags) {
			if (typeof newInfo.titleChunk !== 'undefined') {
				this.$root.title = newInfo.titleChunk;
			}
		},
	},
};
</script>
