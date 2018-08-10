const path = require('path');

function resolve(dir) {
	return path.join(__dirname, dir);
}

module.exports = {
	resolve: {
		extensions: ['.js', '.vue', '.json'],
		alias: {
			vue$: 'vue/dist/vue.runtime.esm.js',
			'@': resolve('src'),
		},
	},
};
