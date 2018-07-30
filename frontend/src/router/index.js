import Vue from 'vue';
import Router from 'vue-router';
import store from '../store';
import Home from '@/components/home/home';
import About from '@/components/about/about';
import StatusList from '@/components/status/list/app';
import StatusDetail from '@/components/status/detail/app';
import Contest from '@/components/contest/contest';
import BlogList from '@/components/blog/list/app';
import BlogEditor from '@/components/blog/basic/app';
import UserList from '@/components/user/list/app';
import UserDetail from '@/components/user/detail/app';
import UserSettings from '@/components/user/settings/app';
import Login from '@/components/signin/login';
import Signup from '@/components/signin/signup';
import Signout from '@/components/signin/signout';
import NotFound from '@/components/global/404';
import ProblemList from '@/components/problem/list/app';
import ProblemDetail from '@/components/problem/detail/app';
import ProblemDescription from '@/components/problem/detail/description';
import ProblemEditor from '@/components/problem/detail/editor';
import ProblemDiscussion from '@/components/problem/detail/discussion';
import ProblemEdit from '@/components/problem/detail/edit';

Vue.use(Router);

const ifNotAuthenticated = (to, from, next) => {
	if (!store.getters['user/isAuthenticated']) {
		next();
		return;
	}
	next('/');
};

const ifAuthenticated = (to, from, next) => {
	if (store.getters['user/isAuthenticated']) {
		next();
		return;
	}
	next('/login');
};

export default new Router({
	mode: 'history',
	routes: [
		{
			path: '',
			redirect: {
				name: 'Home',
			},
		},
		{
			path: '/home',
			name: 'Home',
			component: Home,
		},
		{
			path: '/login',
			name: 'Login',
			component: Login,
			beforeEnter: ifNotAuthenticated,
		},
		{
			path: '/status',
			name: 'Status',
			component: StatusList,
		},
		{
			path: '/status/:pk',
			name: 'StatusDetail',
			component: StatusDetail,
		},
		{
			path: '/contest',
			name: 'Contest',
			component: Contest,
		},
		{
			path: '/user',
			name: 'User',
			component: UserList,
		},
		{
			path: '/user/settings',
			name: 'UserSettings',
			component: UserSettings,
			beforeEnter: ifAuthenticated,
		},
		{
			path: '/user/:username',
			name: 'UserDetail',
			component: UserDetail,
		},
		{
			path: '/blog',
			name: 'Blog',
			component: BlogList,
		},
		{
			path: '/blog/create',
			name: 'BlogCreate',
			component: BlogEditor,
			beforeEnter: ifAuthenticated,
		},
		{
			path: '/about',
			name: 'About',
			component: About,
		},
		{
			path: '/signup',
			name: 'Signup',
			component: Signup,
			beforeEnter: ifNotAuthenticated,
		},
		{
			path: '/signout',
			name: 'Signout',
			component: Signout,
			beforeEnter: ifAuthenticated,
		},
		{
			path: '/problem',
			name: 'Problem',
			component: ProblemList,
		},
		{
			path: '/problem/:slug/edit',
			name: 'ProblemEdit',
			component: ProblemEdit,
		},
		{
			path: '/problem/:slug',
			component: ProblemDetail,
			children: [
				{
					path: 'description',
					name: 'ProblemDetailDescription',
					component: ProblemDescription,
				},
				{
					path: 'editor',
					name: 'ProblemDetailEditor',
					component: ProblemEditor,
				},
				{
					path: 'discussion',
					name: 'ProblemDetailDiscussion',
					component: ProblemDiscussion,
				},
			],
		},
		{
			path: '*',
			name: '404',
			component: NotFound,
		},
	],
});
