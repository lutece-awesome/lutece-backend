<!--
    Homepage
-->
<template>
	<div class = "hone">
		<div class = "ui grid">
			<div class = "eight wide column">
				<div class="ui attached message">
					<div class="header">Announcements</div>
				</div>
				<div class="ui attached segment"/>
			</div>

			<div class = "eight wide column">
				<div class="ui attached message">
					<div class="header">Top Solved</div>
				</div>
				<div class="ui attached ">
					<table
						class="ui attached padded celled table"
						style = "text-align:center;">
						<tr>
							<th style = "width:1em;">#</th>
							<th style = "width:2em;">User</th>
							<th style = "width:1em">Solved</th>
						</tr>
						<td
							v-for = "each_user in top_user"
							:key = "each_user.id"/>
					</table>

				</div>
			</div>
		</div>
	</div>

</template>

<script>
export default {
	data: function () {
		return {
			top_user: []
		}
	}
}
</script>
