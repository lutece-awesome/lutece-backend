<template>
	<v-layout
		row
		wrap>
		<v-flex
			xs12
			sm4>
			<v-select
				v-model = "language"
				:items = "items"
				width="100"/>
		</v-flex>

		<v-flex
			xs12
			sm10>
			<codemirror
				v-model = "code"
				:options = "cmOptions"
			/>
		</v-flex>


	</v-layout>
</template>

<script>
import { codemirror } from 'vue-codemirror';
import 'codemirror/lib/codemirror.css';
import 'codemirror/addon/selection/active-line';
import 'codemirror/keymap/sublime';
import 'codemirror/addon/edit/closebrackets';

export default {
	components: {
		codemirror,
	},
	data: () => ({
		cmOptions: {
			indentUnit: 4,
			lineNumbers: true,
			keyMap: 'sublime',
			tabindex: '0',
			line: true,
			styleActiveLine: true,
			matchBrackets: true,
		},
		code: '',
		language: {
			text: 'GNU G++17',
			value: 'GNU G++',
		},
		items: [{
			text: 'GNU G++17',
			value: 'GNU G++',
		},
		{
			text: 'GNU GCC 7.3',
			value: 'GNU GCC',
		},
		{
			text: 'Clang 6.0.0',
			value: 'Clang',
		},
		{
			text: 'Python 3.6.5',
			value: 'Python',
		},
		{
			text: 'Java 10',
			value: 'Java',
		},
		{
			text: 'Go 1.10.2',
			value: 'Go',
		},
		{
			text: 'Ruby 2.5.1',
			value: 'Ruby',
		},
		{
			text: 'Rust 1.26.1',
			value: 'Rust',
		}],
	}),
};
</script>
