<template>
    <v-layout row wrap justify-center>
        <v-flex xs12>
            <v-card>
                <v-toolbar card prominent tabs>
                    <v-toolbar-title>
                        A PLUS B
                    </v-toolbar-title>
                    <v-tabs v-model="tabs" color="transparent" slot="extension">
                        <v-tab :ripple='false' to="description">Description</v-tab>
                        <v-tab :ripple='false' to="editor">Editor</v-tab>
                        <v-tab :ripple='false' to="discussion">Discussion</v-tab>
                    </v-tabs>
                </v-toolbar>
                <v-tabs-items touchless v-model="tabs">
                    <v-tab-item id="description">
                        <ProblemDescription/>
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
    export default {
        components: {
            ProblemDescription,
            ProblemEditor,
            ProblemDiscussion,
        },
        data: () => ({
            tabs: "",
        }),
    }
</script>
