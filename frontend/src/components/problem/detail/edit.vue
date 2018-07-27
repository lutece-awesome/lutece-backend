</<template>
    <v-form>
        <v-container>
            <v-layout row wrap justify-center>
                <v-flex xs12 md10>
                    <v-text-field
                        v-model="title"
                        label="Title"
                    />

                    <v-text-field
                        v-model="timeLimit"
                        type= "number"
                        label="TimeLimit"
                    />

                    <v-text-field
                        v-model="memoryLimit"
                        type= "number"
                        label="MemoryLimit"
                    />

                    <v-switch
                        v-model="visible"
                        :label = "visible ? 'Visible' : 'Invisible'"
                    />

                    <v-switch
                        v-model="discussionvisible"
                        :label = "discussionvisible ? 'DiscussionVisible' : 'DiscussionInvisible'"
                    />

                    <p> UPLOAD TO DO </p>

                    <v-textarea
                        :value= "content"
                    />
                    <div
                        v-mixrend = "content"
                        class="mb-3" />

                    <v-textarea
                        :value= "standardInput"
                    />
                    <div
                        v-mixrend = "standardInput"
                        class="mb-3" />

                    <v-textarea
                        :value= "standardOutput"
                    />
                    <div
                        v-mixrend = "standardOutput"
                        class="mb-3" />
                    <v-textarea
                        :value= "constraints"
                    />
                    <div
                        v-mixrend = "constraints"
                        class="mb-3" />

                    <v-textarea
                        :value= "note"
                    />
                    <div
                        v-mixrend = "note"
                        class="mb-3" />

                    <v-text-field
                        v-model="resource"
                        label="resource"
                    />

                    <div v-for = "(each , index) in samples" :key = "index">
                        <span>
                            {{ each.input }}
                        </span>
                        <span>
                            {{ each.output }}
                        </span>
                    </div>

                    <v-btn> ADD SAMPLE </v-btn>

                    <v-btn> SUBMIT </v-btn>

                </v-flex>
            </v-layout>
        </v-container>
    </v-form>
</template>


<script>
export default {
	props: {
		title: {
			type: String,
			default: '',
		},
		timeLimit: {
			type: Number,
			default: 2000,
		},
		memoryLimit: {
			type: Number,
			default: 128,
		},
		visible: {
			type: Boolean,
			default: false,
		},
		discussionvisible: {
			type: Boolean,
			default: false,
		},
		content: {
			type: String,
			default: '',
		},
		standardInput: {
			type: String,
			default: '',
		},
		standardOutput: {
			type: String,
			default: '',
		},
		constraints: {
			type: String,
			default: '',
		},
		samples: {
			type: Array,
			default: () => [],
		},
		note: {
			type: String,
			default: '',
		},
		resource: {
			type: String,
			default: '',
		},
	},

	methods: {

		submit() {

		},

	},
};
</script>
