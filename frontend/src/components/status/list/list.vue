<template>
	<v-data-table
		:items="statusItem"
		:loading="isLoading"
		:headers-length="8"
		hide-actions >
		<template
			slot="items"
			slot-scope="props">
			<router-link
				:to="{name: 'StatusDetail', params: {pk: props.item.submissionId}}"
				:style="{cursor: 'pointer'}"
				tile
				tag="tr">
				<td class="text-xs-center">{{ props.item.submissionId }}</td>
				<td class="text-xs-center nowrap">
					<v-avatar
						size="32"
						class="mr-1" >
						<img :src="props.item.user.gravataremail" >
					</v-avatar>
					{{ props.item.user.displayName }}
				</td>
				<td class="text-xs-center">{{ props.item.problem.title }}</td>
				<td
					:class="props.item.color + '--text'"
					class="text-xs-center">
					{{ props.item.judgeStatus }}
					<span v-if="props.item.failedCase">#{{ props.item.failedCase }}</span>
				</td>
				<td class="text-xs-center">{{ props.item.timeCost }}</td>
				<td class="text-xs-center">{{ props.item.memoryCost }}</td>
				<td class="text-xs-center time">
					<span class="humanize-time">{{ props.item.submitTime | moment("from") }}</span>
					<span class="full-time">{{ props.item.submitTime | moment("Y-MM-DD HH:mm:ss") }}</span>
				</td>
				<td class="text-xs-center">{{ props.item.language }}</td>
			</router-link>
		</template>
		<template
			slot="headers"
			slot-scope="props">
			<tr>
				<th
					role="columnheader"
					scope="col"
					class="column text-xs-center">
					<v-text-field
						v-model="filters.pk"
						label="#"
						single-line
						hide-details
						type="number"
						min="1"
						step="1"
						style="width: 50px"
					/>
				</th>
				<th
					role="columnheader"
					scope="col"
					class="column text-xs-center">
					<v-autocomplete
						v-model="filters.user"
						:items="userSearch.items"
						:loading="userSearch.isLoading"
						:search-input.sync="userSearch.filter"
						:append-icon="null"
						single-line
						hide-details
						clearable
						label="User"
						style="width: 80px"
						item-text="name"
						dense
					/>

				</th>
				<th
					role="columnheader"
					scope="col"
					class="column text-xs-center">
					<v-autocomplete
						v-model="filters.problem"
						:items="problemSearch.items"
						:loading="problemSearch.isLoading"
						:search-input.sync="problemSearch.filter"
						:append-icon="null"
						single-line
						hide-details
						clearable
						label="Problem"
						style="width: 120px"
						item-text="name"
						dense
					/>
				</th>
				<th
					role="columnheader"
					scope="col"
					class="column text-xs-center">
					<v-select
						v-model="filters.judgeStatus"
						:items="verdictItems"
						label="Verdict"
						single-line
						hide-details
						dense
						clearable
						offset-y
						style="width: 180px"
					/>
				</th>
				<th
					role="columnheader"
					scope="col"
					class="column text-xs-center">Time (ms)</th>
				<th
					role="columnheader"
					scope="col"
					class="column text-xs-center">Memory (KiB)</th>
				<th
					role="columnheader"
					scope="col"
					class="column text-xs-center">Submit Time</th>
				<th
					role="columnheader"
					scope="col"
					class="column text-xs-center">
					<v-select
						v-model="filters.language"
						:items="languageItems"
						label="Language"
						single-line
						hide-details
						dense
						clearable
						offset-y
						style="width: 100px"
					/>
				</th>
			</tr>
		</template>
	</v-data-table>
</template>


<script>
export default {
	props: {
		statusItem: {
			type: Array,
			default: () => [],
		},
		isLoading: {
			type: Boolean,
			default: false,
		},
		filters: {
			type: Object,
			default: () => {},
		},
		userSearch: {
			type: Object,
			default: () => {},
		},
		problemSearch: {
			type: Object,
			default: () => {},
		},
	},
	data: () => ({
		verdictItems: [
			'Pending',
			'Preparing',
			'Accepted',
			'Running',
			'Compile Error',
			'Wrong Answer',
			'Runtime Error',
			'Time Limit Exceeded',
			'Output Limit Exceeded',
			'Memory Limit Exceeded',
			'Judger Error',
		],
		languageItems: [
			'GNU G++',
			'GNU GCC',
			'Clang',
			'Python',
			'Java',
			'Go',
			'Ruby',
			'Rust',
		],
	}),
};
</script>
