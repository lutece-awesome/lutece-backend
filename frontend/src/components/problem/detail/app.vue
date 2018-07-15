<template>
    <v-layout row wrap justify-center>
        <v-flex xs12 md9>
            <v-card>
                <v-toolbar card prominent tabs>
                    <v-toolbar-title>
                        A PLUS B
                    </v-toolbar-title>
                    <v-tabs color="transparent" slot="extension">
                        <v-tab :ripple='false' to = 'description' >Description</v-tab>
                        <v-tab :ripple='false' to = 'editor' >Editor</v-tab>
                        <v-tab :ripple='false' to = 'discussion' >Discussion</v-tab>
                    </v-tabs>
                </v-toolbar>

                <v-card-text>
                    <router-view />
                </v-card-text>
                
            </v-card>
        </v-flex>
    </v-layout>            
</template>


<script>

    export default {
        data: () => ({
            slug: '',
        }),

        mounted(){
            this.slug = this.$route.params.slug;
            this.$router.push( 'description' );
        },

        methods:{
            Description(){
                this.$router.push({
                    name: 'ProblemDetailDescription',
                    params:{
                        slug: this.slug
                    }
                })
            },



        }
    }
</script>
