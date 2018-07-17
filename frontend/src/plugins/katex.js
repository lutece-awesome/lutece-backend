// import katex from 'katex';
import renderMathInElement from 'katex/contrib/auto-render/auto-render';

export default {
	install(Vue, _options) {
		Vue.directive('katex', (el, binding) => {
			// const displayStyle = binding.arg === 'display';
			// const expression = binding.value.expression ? binding.value.expression : binding.value;
			if (binding.value.expression) {
				if (binding.value.options) {
					renderMathInElement(
						el,
						...binding.value.options,
					);
				} else {
					renderMathInElement(
						el,
					);
				}
			} else {
				// console.log(el);
				renderMathInElement(
					el,
					{
						delimiters: [
							{ left: '$$', right: '$$', display: true },
							{ left: '$', right: '$', display: false },
							{ left: '\\[', right: '\\]', display: true },
							{ left: '\\(', right: '\\)', display: false },
						],
					},
				);
			}
		});
	},
};
