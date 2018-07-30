const path = require('path');
const webpack = require('webpack');
const merge = require('webpack-merge');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const FontminPlugin = require('fontmin-webpack');
const PurgecssPlugin = require('purgecss-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const glob = require('glob-all');
const _ = require('lodash');
const FaviconsWebpackPlugin = require('favicons-webpack-plugin');
const safeParser = require('postcss-safe-parser');
const baseWebpackConfig = require('./webpack.base.conf');
const config = require('../config');
const utils = require('./utils');
const env = require('../config/prod.env');

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

const webpackConfig = merge(baseWebpackConfig, {
	mode: 'production',
	module: {
		rules: utils.styleLoaders({
			sourceMap: config.build.productionSourceMap,
			extract: true,
			usePostCSS: true,
		}),
	},
	devtool: config.build.productionSourceMap ? config.build.devtool : false,
	output: {
		path: config.build.assetsRoot,
		filename: utils.assetsPath('js/[name].[chunkhash].js'),
	},
	plugins: [
		// http://vuejs.github.io/vue-loader/en/workflow/production.html
		new webpack.DefinePlugin({
			'process.env': env,
		}),
		// extract css into its own file
		new MiniCssExtractPlugin({
			filename: utils.assetsPath('css/[name].[chunkhash].css'),
		}),
		new PurgecssPlugin({
			paths: glob.sync([
				path.join(__dirname, './../index.html'),
				path.join(__dirname, './../src/**/*.vue'),
				path.join(__dirname, './../src/**/*.js'),
				path.join(__dirname, '..', 'node_modules', 'vuetify', 'src', '**/*.@(js|ts)'),
			]),
			whitelist: ['mord'],
			whitelistPatterns: [/^v-progress-circular/, /transition/, /^vch__/],
			whitelistPatternsChildren: [/katex/, /CodeMirror/, /codemirror/, /cm-/, /v-input/],
		}),
		// Compress extracted CSS. We are using this plugin so that possible
		// duplicated CSS from different components can be deduped.
		new OptimizeCSSAssetsPlugin({
			cssProcessorOptions: config.build.productionSourceMap
				? { parser: safeParser, map: { inline: false } }
				: { parser: safeParser },
		}),
		// generate dist index.html with correct asset hash for caching.
		// you can customize output by editing /index.html
		// see https://github.com/ampedandwired/html-webpack-plugin
		new HtmlWebpackPlugin({
			filename: config.build.index,
			template: 'index.html',
			inject: true,
			minify: {
				removeComments: true,
				collapseWhitespace: true,
				removeAttributeQuotes: true,
				// more options:
				// https://github.com/kangax/html-minifier#options-quick-reference
			},
			// necessary to consistently work with multiple chunks
			chunksSortMode: 'dependency',
		}),
		new FaviconsWebpackPlugin({
			logo: path.join(__dirname, 'logo.svg'),
			prefix: 'static/icons-[hash:8]/',
			title: 'Lutece',
			icons: {
				appleIcon: { offset: 10 },
				windows: { background: 'transparent' },
			},
			// config: {
			// 	appName: 'Lutece',
			// 	background: '#1e88e5',
			// 	theme_color: '#1e88e5',
			// 	start_url: '/home',
			// },
		}),
		// keep module.id stable when vendor modules does not change
		new webpack.NamedChunksPlugin(),
		new webpack.HashedModuleIdsPlugin(),
		// copy custom static assets
		new CopyWebpackPlugin([
			{
				from: path.resolve(__dirname, '../static'),
				to: config.build.assetsSubDirectory,
				ignore: ['.*'],
			},
		]),
		new MyFontminPlugin({
			autodetect: true,
		}),
	],
	optimization: {
		splitChunks: {
			chunks: 'all',
		},
		minimizer: [
			new UglifyJsPlugin({
				uglifyOptions: {
					compress: {
						warnings: false,
					},
				},
				sourceMap: config.build.productionSourceMap,
				parallel: true,
			}),
		],
	},
});

if (config.build.productionGzip) {
	const CompressionWebpackPlugin = require('compression-webpack-plugin');

	webpackConfig.plugins.push(
		new CompressionWebpackPlugin({
			asset: '[path].gz[query]',
			algorithm: 'gzip',
			test: new RegExp(
				`\\.(${
					config.build.productionGzipExtensions.join('|')
				})$`,
			),
			threshold: 10240,
			minRatio: 0.8,
		}),
	);
}

if (config.build.bundleAnalyzerReport) {
	const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
	webpackConfig.plugins.push(new BundleAnalyzerPlugin());
}

module.exports = webpackConfig;
