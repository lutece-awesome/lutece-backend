/* eslint no-param-reassign: ["error", { "props": false }] */

export default {
	install(Vue) {
		const mdPromise = new Promise(((resolve, _reject) => {
			import('markdown-it').then(({ default: MD }) => {
				import('@neilsustc/markdown-it-katex').then(({ default: mk }) => {
					const md = MD();
					md.use(mk);
					resolve(md);
				});
			});
		}));
		Vue.directive('mixrend', (el, binding) => {
			mdPromise.then((md) => {
				if (binding.value.expression) {
					el.innerHTML = md.render(binding.value.expression);
				} else {
					el.innerHTML = md.render(binding.value);
				}
			});
		});
	},
};
