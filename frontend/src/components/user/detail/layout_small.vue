<template>
	<v-container justify-center>
		<v-layout
			row
			wrap>
			<v-flex xs12>
				<user-profile :user = "user" />
			</v-flex>
			<v-flex
				xs12
				class = "mt-4"
			>
				<user-summary :user = "user" />
			</v-flex>
		</v-layout>
</v-container></template>


<script>

import UserProfile from '@/components/user/detail/profile';
import UserSummary from '@/components/user/detail/summary';

export default {
	components: {
		UserProfile,
		UserSummary,
	},

	props: {
		user: {
			type: Object,
			default: null,
		},
	},
};
</script>
