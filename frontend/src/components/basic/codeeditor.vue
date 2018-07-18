<template>
	<v-layout
		row
		wrap>
		<v-flex xs12>
			<codemirror
				ref="codeMirror"
				v-model = "code"
				:options = "cmOptions"
			/>
		</v-flex>
		<v-flex xs12>
			<v-card-actions class="v-toolbar">
				<v-select
					v-model = "language"
					:items = "items"
					label="Language"
					hide-details
				/>
				<v-spacer/>
				<v-btn
					large
					flat
					type="submit">Submit</v-btn>
			</v-card-actions>
		</v-flex>
	</v-layout>
</template>

<script>
import { codemirror } from 'vue-codemirror';
import 'codemirror/lib/codemirror.css';
import 'codemirror/addon/selection/active-line';
import 'codemirror/keymap/sublime';
import 'codemirror/addon/edit/closebrackets';
import 'codemirror/mode/clike/clike';
import 'codemirror/mode/go/go';
import 'codemirror/mode/rust/rust';
import 'codemirror/mode/ruby/ruby';
import 'codemirror/mode/python/python';
import { LanguageList } from '@/graphql/language/languagelist.gql';

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
			mode: '',
		},
		code: '',
		language: '',
		items: [],
	}),

	watch: {
		language() {
			for (let i = 0; i < this.items.length; i += 1) {
				if (this.items[i].value === this.language) {
					this.cmOptions.mode = this.items[i].codemirror;
				}
			}
		},
	},

	mounted() {
		this.$apollo.query({
			query: LanguageList,
		})
			.then(response => JSON.parse(response.data.allLanguage))
			.then((data) => {
				this.data = [];
				for (let i = 0; i < data.length; i += 1) {
					const {
						full, info,
					} = data[i];
					this.items.push({ text: info, value: full, codemirror: data[i].codemirror });
				}
				this.language = this.items[0].value;
			});
	},

};
</script>
