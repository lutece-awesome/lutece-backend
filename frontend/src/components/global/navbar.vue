<template>
	<div>
		<v-navigation-drawer
			v-model="drawer"
			:width="240"
			fixed
			clipped
			app>
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
			<v-toolbar-title>
				Lutece
			</v-toolbar-title>
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
						<v-list-tile @click="signout">
							<v-icon class="mr-2">mdi-logout</v-icon>
							<v-list-tile-content>
								<v-list-tile-title>Sign Out</v-list-tile-title>
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
import { verifyToken } from '@/graphql/signin/token.gql';

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
	},
	watch: {
		authed(val) {
			if (val === false) { this.refresh(); }
		},
	},
	mounted() {
		this.refresh();
	},
	methods: {
		refresh() {
			if (!localStorage.getItem('USER_TOKEN')) return;
			this.logging = true;
			this.$apollo
				.mutate({
					mutation: verifyToken,
					variables: {
						token: localStorage.getItem('USER_TOKEN') || '',
					},
				})
				.then(response => response.data.verifyToken.payload)
				.then((data) => {
					this.$store.commit('user/update_authed', true);
					this.$store.commit('user/update_gravataremail', data.gravataremail);
					this.$store.commit('user/update_displayname', data.displayname);
				})
				.finally(() => { this.logging = false; });
		},
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
	},
};
</script>
