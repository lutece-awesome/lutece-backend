<script>
export default {
	metaInfo() { return { title: this.loadingmsg }; },
	props: {
		loadingmsg: {
			type: String,
			default: 'Loading...',
		},
	},
	data() {
		return {
			isLoading: true,
		};
	},
};
</script>
