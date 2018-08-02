<template>
	<div>
		<div>
			<v-icon class = "mr-1" > mdi-comment </v-icon>
			<span style = "font-size:16px;font-weight:500;" > Comments: </span>
		</div>

		<v-container>
			<v-card>
				<div class = "pl-2 pr-2" >
					<v-card-text
						class = "mb-4" >
						<div>
							<v-avatar size = "40" >
								<img src = "https://secure.gravatar.com/avatar/79bc21937a1f625d1cf08c919f8c70c2.jpg?r=g&s=300&d=mm" >
							</v-avatar>
							<a class = "ml-1" > xiper </a>
							<span class = "ml-2" >
								<v-icon small>
									mdi-clock
								</v-icon>
								5 hours ago
							</span>
						</div>
						<div class = "mt-3" >
							海葬DLC第二章很像是一场献给海底城和天空城时代《生化奇兵》的送别——一场精心布置的、令人苦苦思索的送别。
							如果这真的就是最后的结局，那么这场从海底到天空、又从天空返回海底的旅程实在是让人难以忘怀。而且，伊丽莎白再一次告诉了我们，
							无论如何，在某处总有一座灯塔、有一个男人、有一座城市……
						</div>

						<div class = "mb-0 mt-3">
							<span> 5 </span>
							<span class = "ml-1" >
								<v-icon small>
									mdi-chevron-up
								</v-icon>
							</span>
							<span>
								<v-icon small>
									mdi-chevron-down
								</v-icon>
							</span>
							<span class = "ml-2 mr-2" > | </span>
							<span> Reply </span>
						</div>
					</v-card-text>
				</div>
			</v-card>
		</v-container>
	</div>
</template>

<script>
export default {

};
</script>
