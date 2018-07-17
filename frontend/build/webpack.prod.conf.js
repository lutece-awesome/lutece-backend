

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
const baseWebpackConfig = require('./webpack.base.conf');
const config = require('../config');
const utils = require('./utils');

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
		chunkFilename: utils.assetsPath('js/[id].[chunkhash].js'),
	},
	plugins: [
		new UglifyJsPlugin({
			uglifyOptions: {
				compress: {
					warnings: false,
				},
			},
			sourceMap: config.build.productionSourceMap,
			parallel: true,
		}),
		new MiniCssExtractPlugin({
			filename: utils.assetsPath('css/[name].[hash].css'),
			chunkFilename: utils.assetsPath('css/[id].[hash].css'),
		}),
		new PurgecssPlugin({
			paths: glob.sync([
				path.join(__dirname, './../index.html'),
				path.join(__dirname, './../src/**/*.vue'),
				path.join(__dirname, './../src/**/*.js'),
				path.join(__dirname, '..', 'node_modules', 'vuetify', 'src', '**/*.@(js|ts)'),
			]),
			whitelistPatterns: [/^v-progress-circular/, /transition/],
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
			// necessary to consistently work with multiple chunks via CommonsChunkPlugin
			chunksSortMode: 'dependency',
		}),
		// keep module.id stable when vendor modules does not change
		new webpack.HashedModuleIdsPlugin(),
		new CopyWebpackPlugin([
			{
				from: path.resolve(__dirname, '../static'),
				to: config.build.assetsSubDirectory,
				ignore: ['.*'],
			},
		]),
		new FontminPlugin({
			autodetect: false,
			glyphs: [
				'\uF00E',
				'\uF026',
				'\uF05D',
				'\uF128',
				'\uF12C',
				'\uF5E0',
				'\uF131',
				'\uF132',
				'\uF140',
				'\uF141',
				'\uF142',
				'\uF764',
				'\uF156',
				'\uF159',
				'\uF205',
				'\uF2DC',
				'\uF2FC',
				'\uF342',
				'\uF343',
				'\uF349',
				'\uF35C',
				'\uF35D',
				'\uF375',
				'\uF3EB',
				'\uF43D',
				'\uF43E',
				'\uF538',
				'\uF572',
			],
		}),
	],
	optimization: {
		splitChunks: {
			chunks: 'all',
		},
		minimizer: [
			new OptimizeCSSAssetsPlugin({}),
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
