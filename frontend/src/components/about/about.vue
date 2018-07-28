<template>
	<v-container fluid>
		<div>
			<h1
				class="headline mb-3 primary--text">Introduction</h1>
			<p><b>Lutece</b>(卢特斯)是一个基于GNU General Public License Version 3协议开源的Online Judge.</p>
			<p><b>Lutece</b>的名字取自<a href = "https://en.wikipedia.org/wiki/BioShock_Infinite">BioShock Infinite</a>
				中的双胞胎科学家(事实上她们是同一个人)Robert Lutece和Rosalind Lutece的姓氏.</p>
			<p><b>Lutece</b>不仅将支持传统算法,还将计划支持并行计算和机器学习.</p>
			<h1
				class="headline mb-3 primary--text">Author</h1>
			<v-container
				fluid
				grid-list-lg
				class="pa-0 mb-3">
				<v-layout
					row
					wrap
				>
					<v-flex
						xs12
						sm6
						md4
						xl3>
						<v-card>
							<v-container
								fluid
								grid-list-lg>
								<v-layout row>
									<v-flex xs7>
										<div>
											<div class="headline">Ke Shen</div>
											<div>Google</div>
											<div>Software Engineer</div>
										</div>
										<v-btn
											icon
											href="https://github.com/LaPluses"
											class="mx-0">
											<v-icon class="mdi-36px">mdi-github-circle</v-icon>
										</v-btn>
									</v-flex>
									<v-flex xs5>
										<v-card-media
											src="https://secure.gravatar.com/avatar/79bc21937a1f625d1cf08c919f8c70c2.jpg?r=g&amp;s=300&amp;d=mm"
											height="125px"
											contain
										/>
									</v-flex>
								</v-layout>
							</v-container>
						</v-card>
					</v-flex>
					<v-flex
						xs12
						sm6
						md4
						xl3>
						<v-card>
							<v-container
								fluid
								grid-list-lg>
								<v-layout row>
									<v-flex xs7>
										<div>
											<div class="headline">Zhu He</div>
											<div>Alibaba</div>
											<div>Algorithm Engineer</div>
										</div>
										<v-btn
											icon
											href="https://github.com/holdzhu"
											class="mx-0">
											<v-icon class="mdi-36px">mdi-github-circle</v-icon>
										</v-btn>
									</v-flex>
									<v-flex xs5>
										<v-card-media
											src="https://secure.gravatar.com/avatar/ec21fbe82157f45b8cab83f91f0cac69.jpg?r=g&amp;s=300&amp;d=mm"
											height="125px"
											contain
										/>
									</v-flex>
								</v-layout>
							</v-container>
						</v-card>
					</v-flex>
				</v-layout>
			</v-container>
			<h1
				class="headline mb-3 primary--text">Contributor</h1>
			<v-container
				fluid
				grid-list-lg
				class="pa-0 mb-3">
				<v-layout
					row
					wrap
				>
					<v-flex
						xs12
						sm6
						md4
						xl3>
						<v-card>
							<v-container
								fluid
								grid-list-lg>
								<v-layout row>
									<v-flex xs7>
										<div>
											<div class="headline">Jun Qing</div>
											<div>Bytedance</div>
											<div>Algorithm Engineer</div>
										</div>
										<v-btn
											icon
											href="http://www.cnblogs.com/qscqesze/"
											class="mx-0">
											<v-icon class="mdi-36px">mdi-book-open</v-icon>
										</v-btn>
									</v-flex>
									<v-flex xs5>
										<v-card-media
											src="https://secure.gravatar.com/avatar/647ebdcf8e291dc01e81ddd4e59a33ec.jpg?r=g&amp;s=300&amp;d=mm"
											height="125px"
											contain
										/>
									</v-flex>
								</v-layout>
							</v-container>
						</v-card>
					</v-flex>
				</v-layout>
			</v-container>
			<h1
				class="headline mb-3 primary--text">Copyright</h1>
			<p>
				<b>Lutece</b> Copyright<i class = "copyright icon"/> 2018, Ke Shen(
				<a href = "Mailto:xipersup@gmail.com">xipersup@gmail.com</a> ), Zhu He(
				<a href = "Mailto:hezhu1688@gmail.com">hezhu1688@gmail.com</a> ). All rights reserved.
			</p>
		</div>
	</v-container>
</template>

<script>
export default {
	metaInfo() { return { title: 'About' }; },
};
</script>
