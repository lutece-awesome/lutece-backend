

const path = require('path');
const webpack = require('webpack');
const merge = require('webpack-merge');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
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
		new MiniCssExtractPlugin({
			filename: utils.assetsPath('css/[name].[hash].css'),
			chunkFilename: utils.assetsPath('css/[id].[hash].css'),
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
