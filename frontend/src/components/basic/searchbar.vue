<template>
	<v-hover>
		<v-card
			slot-scope = "{ hover }"
			:class = "`elevation-${hover || isFocus ? 4 : 1}`"
		>
			<v-text-field
				v-model = "input"
				:label = "label"
				hide-details
				prepend-inner-icon = "mdi-magnify"
				solo
				flat
				type = "search"
				@focus = "setFocus"
				@blur = "removeFocus"
			/>
		</v-card>
	</v-hover>
</template>

<script>

const debounce = require('lodash.debounce');

export default {
	props: {
		label: {
			type: String,
			default: 'Search',
		},
		delay: {
			type: Number,
			default: 300,
		},
		callback: {
			type: Function,
			default: () => {},
		},
	},
	data: () => ({
		input: '',
		isFocus: false,
		debounceInput: null,
	}),
	watch: {
		input() {
			this.debounceInput();
		},
	},
	created() {
		this.debounceInput = debounce(this.emit, this.delay);
	},
	methods: {
		emit() {
			this.callback(this.input);
		},
		setFocus() {
			this.isFocus = true;
		},
		removeFocus() {
			this.isFocus = false;
		},
	},
};
</script>
