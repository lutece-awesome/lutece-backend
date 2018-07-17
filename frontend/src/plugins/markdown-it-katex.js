/* eslint no-param-reassign: ["error", { "props": false }] */

const md = require('markdown-it')();
const mk = require('@iktakahiro/markdown-it-katex');

md.use(mk);

export default {
	install(Vue) {
		Vue.directive('mixrend', (el, binding) => {
			if (binding.value.expression) {
				el.innerHTML = md.render(binding.value.expression);
			} else {
				el.innerHTML = md.render(binding.value);
			}
		});
	},
};
