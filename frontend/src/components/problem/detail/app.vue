<template>
    <v-layout row wrap justify-center>
        <v-flex xs8>
            <v-card>
                <v-toolbar card prominent tabs>
                    <v-toolbar-title>
                        {{ title }}
                    </v-toolbar-title>
                    <v-tabs v-model="tabs" color="transparent" slot="extension">
                        <v-tab :ripple='false' to="description">Description</v-tab>
                        <v-tab :ripple='false' to="editor">Editor</v-tab>
                        <v-tab :ripple='false' to="discussion">Discussion</v-tab>
                    </v-tabs>
                </v-toolbar>
                <v-tabs-items touchless v-model="tabs">
                    <v-tab-item id="description">
                        <ProblemDescription :content = content :standardInput = standardInput :standardOutput = standardOutput :constraints = constraints />
                    </v-tab-item>
                    <v-tab-item id="editor">
                        <ProblemEditor/>
                    </v-tab-item>
                    <v-tab-item id="discussion">
                        <ProblemDiscussion/>
                    </v-tab-item>
                </v-tabs-items>
            </v-card>
        </v-flex>
    </v-layout>            
</template>


<script>
    import ProblemDescription from "@/components/problem/detail/description.vue";
    import ProblemEditor from "@/components/problem/detail/editor.vue";
    import ProblemDiscussion from "@/components/problem/detail/discussion.vue";
    import { ProblemDetailGQL } from '@/graphql/problem/detail.js'
    export default {
        components: {
            ProblemDescription,
            ProblemEditor,
            ProblemDiscussion,
        },
        data: () => ({
            slug: '',
            isLoading: false,
            tabs: null,
            title: '',
            content: '',
            standardInput: '',
            standardOutput: '',
            constraints: '',
            resource: '',
            note: '',
            timeLimit: 0,
            memoryLimit: 0
        }),

        mounted(){
            this.slug = this.$route.params.slug;
            this.request();
        },

        methods:{
            request: function(){
                this.$apollo.query({
                    query: ProblemDetailGQL,
                    variables: {
                        slug: this.slug
                    },
                })
                .then( response => response.data.problem )
                .then( data => {
                    this.title = data.title;
                    this.content = data.content;
                    this.standardInput = data.standardInput;
                    this.standardOutput = data.standardOutput;
                    this.constraints = data.constraints;
                    this.resource = data.resource;
                    this.note = data.note;
                    this.timeLimit = data.timeLimit,
                    this.memoryLimit = data.memoryLimit;
                })
            }
        }
    }
</script>
