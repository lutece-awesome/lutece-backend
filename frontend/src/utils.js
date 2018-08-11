function getServerUri(protocol, path) {
	const env = process.env.NODE_ENV;
	const loc = window.location;
	const host = env === 'production' ? loc.host : `${loc.host.split(':')[0]}:8000`;
	let newUri = protocol;
	if (loc.protocol === 'https:') {
		newUri += 's:';
	} else {
		newUri += ':';
	}
	newUri += `//${host}/${path}`;
	return newUri;
}

function getGraphQLUri() {
	return getServerUri('http', 'graphql');
}

function getWebSocketUri() {
	return getServerUri('ws', 'ws');
}

function getThoundNumberic(number) {
	return number < 1000 ? String(number) : `${String((number / 1000).toFixed(1))}K`;
}

export { getGraphQLUri, getWebSocketUri, getServerUri, getThoundNumberic };
