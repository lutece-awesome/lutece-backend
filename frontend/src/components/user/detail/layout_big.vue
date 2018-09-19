<template>
	<v-container>
		<v-layout
			row
			wrap
			justify-center
		>
			<v-flex xs4>
				<user-profile :user = "user" />
			</v-flex>
			<v-flex
				xs6
				class = "ml-4"
			>
				<user-summary :user = "user" />
			</v-flex>
		</v-layout>
	</v-container>
</template>

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
