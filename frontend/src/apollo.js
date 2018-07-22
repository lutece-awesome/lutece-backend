import Vue from 'vue';
import { ApolloClient } from 'apollo-client';
import { createHttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { setContext } from 'apollo-link-context';
import VueApollo from 'vue-apollo';
import fetch from 'unfetch';
import Cookies from 'js-cookie';
import { getGraphQLUri } from '@/utils';

const httpLink = createHttpLink({
	// You should use an absolute URL here
	uri: getGraphQLUri(),
	credentials: 'same-origin',
	fetch,
});

const httpLinkAuth = setContext((_, { headers }) => {
	// get the authentication token from localstorage if it exists
	const token = localStorage.getItem('USER_TOKEN');
	const headersWithCSRF = {
		...headers,
		'X-CSRFToken': Cookies.get('csrftoken'),
	};
	// return the headers to the context so httpLink can read them
	if (token) {
		return {
			headers: {
				...headersWithCSRF,
				Authorization: `JWT ${token}`,
			},
		};
	}
	return {
		headers: {
			...headersWithCSRF,
		},
	};
});

const apolloClient = new ApolloClient({
	link: httpLinkAuth.concat(httpLink),
	cache: new InMemoryCache(),
	connectToDevTools: true,
});

Vue.use(VueApollo);

const apolloProvider = new VueApollo({
	defaultClient: apolloClient,
});

export default apolloProvider;
