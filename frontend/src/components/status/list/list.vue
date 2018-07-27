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
				:to="{name: &quot;StatusDetail&quot;, params: {pk: props.item.submissionId}}"
				:style="{cursor: 'pointer'}"
				tile
				tag="tr">
				<td class="text-xs-center">{{ props.item.submissionId }}</td>
				<td class="text-xs-center nowrap">
					<v-avatar
						size="32"
						class="mr-1" >
						<img :src="props.item.userGravataremail" >
					</v-avatar>
					{{ props.item.user }}
				</td>
				<td class="text-xs-center">{{ props.item.problem }}</td>
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
					<v-text-field
						v-model="filters.user"
						label="User"
						single-line
						hide-details
						style="width: 80px"
					/>
				</th>
				<th
					role="columnheader"
					scope="col"
					class="column text-xs-center">
					<v-text-field
						v-model="filters.problem"
						label="Problem"
						single-line
						hide-details
						style="width: 100px"
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
