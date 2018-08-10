const _ = require('lodash');
const FontminPlugin = require('fontmin-webpack');
const PurgecssPlugin = require('purgecss-webpack-plugin');
const path = require('path');
const glob = require('glob-all');

class MyFontminPlugin extends FontminPlugin {
	findFontFiles(compilation) {
		const regular = this.findRegularFontFiles(compilation);
		const extract = this.findExtractTextFontFiles(compilation);
		return _.filter(_.uniqBy(regular.concat(extract), 'asset'), o => !o.asset.includes('KaTeX'));
	}

	apply(compiler) {
		compiler.hooks.compilation.tap('Fontmin', (compilation) => {
			compilation.hooks.additionalAssets.tap('Fontmin', () => {
				this.onAdditionalAssets(compilation, () => {});
			});
		});
	}
}

module.exports = {
	pwa: {
		name: 'Lutece',
		manifestPath: 'static/icons/manifest.json',
		iconPaths: {
			favicon32: 'static/icons/favicon-32x32.png',
			favicon16: 'static/icons/favicon-16x16.png',
			appleTouchIcon: 'static/icons/apple-touch-icon-152x152.png',
			maskIcon: 'static/icons/safari-pinned-tab.svg',
			msTileImage: 'static/icons/msapplication-icon-144x144.png',
		},
		themeColor: '#1E88E5',
		msTileColor: '#2B5797',
		appleMobileWebAppCapable: 'yes',
		appleMobileWebAppStatusBarStyle: 'black',
	},

	baseUrl: undefined,
	outputDir: undefined,
	assetsDir: 'static',
	runtimeCompiler: undefined,
	productionSourceMap: undefined,
	parallel: undefined,
	css: undefined,
	chainWebpack: (_config) => {
		_config.when(process.env.NODE_ENV === 'production', (config) => {
			config
				.plugins.delete('prefetch').end()
				.plugin('purgecss')
				.use(PurgecssPlugin, [{
					paths: glob.sync([
						path.join(__dirname, './index.html'),
						path.join(__dirname, './src/**/*.vue'),
						path.join(__dirname, './src/**/*.js'),
						path.join(__dirname, 'node_modules', 'vuetify', 'src', '**/*.@(js|ts)'),
					]),
					whitelistPatterns: [/^(?!mdi)/],
				}])
				.after('extract-css')
				.end()
				.plugin('fontmin')
				.use(MyFontminPlugin)
				.end();
		});
	},
};
