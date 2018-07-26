import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/home/home';
import About from '@/components/about/about';
import StatusList from '@/components/status/list/app';
import StatusDetail from '@/components/status/detail/app';
import Contest from '@/components/contest/contest';
import UserList from '@/components/user/list/app';
import UserDetail from '@/components/user/detail/app';
import Login from '@/components/signin/login';
import Signup from '@/components/signin/signup';
import Signout from '@/components/signin/signout';
import NotFound from '@/components/global/404';
import ProblemList from '@/components/problem/list/app';
import ProblemDetail from '@/components/problem/detail/app';
import ProblemDescription from '@/components/problem/detail/description';
import ProblemEditor from '@/components/problem/detail/editor';
import ProblemSubmission from '@/components/problem/detail/submission';
import ProblemDiscussion from '@/components/problem/detail/discussion';

Vue.use(Router);

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
		},
		{
			path: '/status',
			name: 'Status',
			component: StatusList,
			meta: {
				keepAlive: true,
			},
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
			path: '/user/:username',
			name: 'UserDetail',
			component: UserDetail,
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
		},
		{
			path: '/signout',
			name: 'Signout',
			component: Signout,
		},
		{
			path: '/problem',
			name: 'Problem',
			component: ProblemList,
			meta: {
				keepAlive: true,
			},
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
					path: 'submission',
					name: 'ProblemSubmission',
					component: ProblemSubmission,
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
