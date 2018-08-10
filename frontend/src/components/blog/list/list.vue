<template>
	<div>
		<v-card>
			<div
				class = "ml-2"
			>
				<span>
					<v-avatar
						size = "40"
						class = "mt-2 mb-2 mr-2"
					>
						<img src = "https://secure.gravatar.com/avatar/79bc219….jpg?r=g&d=mm&s=250">
					</v-avatar>
					<a>123</a>
				</span>
			</div>
			<!-- <v-list two-line>
			<v-list-tile>
				<v-list-tile-avatar>
					<img src = "https://secure.gravatar.com/avatar/79bc219….jpg?r=g&d=mm&s=250">
				</v-list-tile-avatar>
				<v-list-tile-content>
					<v-list-tile-title style = "font-size:20px;" > 123456 </v-list-tile-title>
				</v-list-tile-content>
				<v-list-tile-action>
					<v-list-tile-action-text style = "font-size:14px;" >18, Aug, 2018</v-list-tile-action-text>
				</v-list-tile-action>
			</v-list-tile>
			<v-divider/>
			<div>
				<span> 123 </span>
			</div>
		</v-list> -->
			<!-- <v-data-table
			:items = "items"
			:headers = "headers"
			:loading="isLoading"
			hide-actions
		>
			<template
				slot="items"
				slot-scope="props">
				<router-link
					:to="{name: 'BlogDetail', params: {slug: props.item.slug }}"
					:style="{cursor: 'pointer'}"
					tile
					tag="tr">
					<td class="text-xs-center">{{ props.item.id }}</td>
					<td class="text-xs-center">{{ props.item.title }}</td>
					<td class="text-xs-center">{{ props.item.vote }}</td>
					<td class="text-xs-center">{{ props.item.view }}</td>
				</router-link>
			</template>
		</v-data-table> -->
		</v-card>
	</div>
</template>


<script>
export default {
	props: {
		items: {
			type: Array,
			default: () => [],
		},
		isLoading: {
			type: Boolean,
			default: false,
		},
	},
};
</script>
