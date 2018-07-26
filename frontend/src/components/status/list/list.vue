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
						label="#"
						single-line
						hide-details
						style="width: 40px"
					/>
				</th>
				<th
					role="columnheader"
					scope="col"
					class="column text-xs-center">
					<v-text-field
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
	},
	data: () => ({
		hidden: false,
		verdictItems: [
			'Compile Error',
			'Accepted',
			'Memory Limit Exceeded',
		],
		languageItems: [
			'Xiper++',
		],
	}),
};
</script>
