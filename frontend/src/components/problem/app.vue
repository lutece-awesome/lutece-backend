<template>
    <v-layout row justify-center>
        <v-flex xs12 sm6>
            <Loading v-if = "isLoading" loadingstyle = 'ui indeterminate text loader' v-bind:isLoading = 'isLoading' />
            <div v-else>
                <!-- <div class="ui two column stackable grid">
                    <div class = 'left floated column' >
                        <Paginator v-bind:maxpage = maxpage v-bind:page = page v-bind:resolve = resolve />
                    </div>

                    <div class = 'column'>
                        <div style = 'float:right'>
                            <problemsearch placeholder = 'Problem' />
                        </div>
                    </div>
                </div> -->
                <!-- <div style = 'margin-top:20px;' > -->
                <v-flex>
                    <ProblemList v-bind:problemItem = 'problemItem' />
                </v-flex>
                <v-flex>
                    <div class="text-xs-center pt-2">
                        <v-pagination v-model = page :length = maxpage ></v-pagination>
                    </div>
                </v-flex>
                <!-- </div> -->
            </div>
        </v-flex>
    </v-layout>
</template>

<script>
    import ProblemList from '@/components/problem/list.vue'
    import Loading from '@/components/basic/loading.vue'
    import problemsearch from '@/components/basic/problemsearch.vue'
    import { ProblemListGQL } from '@/graphql/problem/list.js'
    export default {

        components:{
            ProblemList,
            Loading,
            problemsearch
        },

        data: function(){
            return {
                isLoading: true,
                page : 0,
                maxpage: 0,
                problemItem : []
            }
        },

        mounted(){
            const pre = localStorage.getItem('PROBLEM_LIST') || 1;
            this.request( pre );
        },

        watch:{
            page: function(){
                this.request( this.page );
            },
        },

        methods:{
            request: function( page ){
                this.isLoading = true;
                this.page = parseInt(page);
                this.$apollo.query({
                    query: ProblemListGQL,
                    variables:{
                        page: this.page
                    },
                }).then( response => response.data.problemList )
                   .then( data => { this.problemItem = data.problemList , this.maxpage = data.maxpage , this.page = Math.min( this.page , this.maxpage ) } )
                   .then( () => this.isLoading = false )
                localStorage.setItem( 'PROBLEM_LIST' , this.page );
            },
        }
    }
</script>
