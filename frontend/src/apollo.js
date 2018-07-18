import Vue from 'vue';
import { ApolloClient } from 'apollo-client';
import { createHttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { setContext } from 'apollo-link-context';
import VueApollo from 'vue-apollo';
import fetch from 'unfetch';

const env = process.env.NODE_ENV;

const httpLink = createHttpLink({
	// You should use an absolute URL here
	uri: env === 'production' ? '/graphql' : 'http://localhost:8000/graphql',
	fetch,
});

const httpLinkAuth = setContext((_, { headers }) => {
	// get the authentication token from localstorage if it exists
	const token = localStorage.getItem('USER_TOKEN');
	// return the headers to the context so httpLink can read them
	if (token) {
		return {
			headers: {
				...headers,
				Authorization: `JWT ${token}`,
			},
		};
	}
	return {
		headers: {
			...headers,
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
