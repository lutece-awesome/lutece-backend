<template>
	<div
		v-if= "isLoading"
		:style = "{ height: height + 'px'}"
		class="ui segment" >
		<div class="ui active inverted dimmer">
			<div :class= "loadingstyle" >{{ loadingmsg }}</div>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		height: {
			type: Number,
			default: 250,
		},
		loadingmsg: {
			type: String,
			default: 'Loading',
		},
		loadingstyle: {
			type: String,
			default: 'ui text loader',
		},
	},
	data() {
		return {
			isLoading: true,
		};
	},
};
</script>
