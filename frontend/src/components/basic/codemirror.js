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
import 'codemirror/theme/neo.css';
import 'codemirror/addon/scroll/simplescrollbars';
import 'codemirror/addon/scroll/simplescrollbars.css';
import 'codemirror/addon/display/autorefresh';

Object.assign(codemirror, {
	beforeDestroy() {
		// TODO: garbage cleanup after transition
	},
});

export default codemirror;
