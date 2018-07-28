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
					v-if="!logging && !authed"
					flat
					@click="login">
					<v-icon class="mr-2">mdi-login</v-icon>
					SIGN IN
				</v-btn>
				<v-menu
					v-if="authed"
					open-on-hover
					offset-y>
					<v-btn
						slot="activator"
						flat>
						<v-avatar
							v-if="authed"
							size="36"
							class="mr-2" >
							<img :src="gravataremail" >
						</v-avatar>
						{{ displayname }}
						<v-icon>mdi-menu-down</v-icon>
					</v-btn>
					<v-list>
						<v-list-tile
							v-for = "( each , index ) in dropdownItems"
							:key = "index"
							@click = "each.click" >
							<v-icon class="mr-2"> {{ each.icon }} </v-icon>
							<v-list-tile-content>
								<v-list-tile-title>{{ each.label }} </v-list-tile-title>
							</v-list-tile-content>
						</v-list-tile>
					</v-list>
				</v-menu>
			</v-toolbar-items>
			<v-btn
				v-if="authed"
				icon
				class="hidden-md-and-up">
				<v-avatar size="36">
					<img :src="gravataremail" >
				</v-avatar>
			</v-btn>
			<v-btn
				v-if="authed"
				icon
				class="hidden-md-and-up"
				@click="signout">
				<v-icon>mdi-logout</v-icon>
			</v-btn>
			<v-btn
				v-if="!logging && !authed"
				icon
				class="hidden-md-and-up"
				@click="login">
				<v-icon>mdi-login</v-icon>
			</v-btn>
		</v-toolbar>
	</div>
</template>

<script>
import Login from '@/components/signin/login';

export default {
	components: {
		Login,
	},
	data() {
		return {
			drawer: null,
			signin: false,
			logging: false,
			items: [{
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
				icon: 'mdi-information',
				title: 'About',
				path: '/about',
			},
			],
			dropdownItems: [
				{
					click: this.profile,
					icon: 'mdi-account',
					label: 'Profile',
				},
				{
					click: this.settings,
					icon: 'mdi-settings',
					label: 'Settings',
				},
				{
					click: this.signout,
					icon: 'mdi-logout',
					label: 'Sign Out',
				},
			],
		};
	},
	computed: {
		authed() {
			return this.$store.state.user.authed;
		},
		gravataremail() {
			return this.$store.state.user.gravataremail;
		},
		displayname() {
			return this.$store.state.user.displayname;
		},
		title() {
			return this.$root.title;
		},
	},
	metaInfo: {
		changed(newInfo, _addedTags, _removedTags) {
			if (typeof newInfo.titleChunk !== 'undefined') {
				this.$root.title = newInfo.titleChunk;
			}
		},
	},
	methods: {
		login() {
			this.$router.push({
				name: 'Login',
				query: {
					redirect: this.$route.path,
				},
			});
		},
		signout() {
			this.$router.push({
				name: 'Signout',
				query: {
					redirect: this.$route.path,
				},
			});
		},
		profile() {
			this.$router.push({
				name: 'UserDetail',
				params: { username: this.$store.state.user.username },
			});
		},
		settings() {
			this.$router.push({
				name: 'UserSettings',
			});
		},
	},
};
</script>
