<template>
    <div>
        <Loading v-if = "isLoading" loadingstyle = 'ui indeterminate text loader' v-bind:isLoading = 'isLoading' />
        <div v-else>
            <div class="ui two column stackable grid">
                <div class = 'left floated column' >
                    <Paginator v-bind:maxpage = maxpage v-bind:page = page v-bind:resolve = resolve />
                </div>

                <div class = 'column'>
                    <div style = 'float:right'>
                        <problemsearch placeholder = 'Problem' />
                    </div>
                </div>
            </div>

            <div style = 'margin-top:20px;' >
                <ProblemList v-bind:problemItem = 'problemItem' />
            </div>
        </div>
    </div>
</template>

<script>
    import Paginator from '@/components/basic/paginator.vue'
    import ProblemList from '@/components/problem/list.vue'
    import Loading from '@/components/basic/loading.vue'
    import problemsearch from '@/components/basic/problemsearch.vue'
    import { ProblemListGQL } from '@/graphql/problem/list.js'
    export default {

        components:{
            Paginator,
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

        methods:{
            request: function( page ){
                localStorage.setItem( 'PROBLEM_LIST' , page );
                this.isLoading = true;
                this.page = parseInt(page);
                this.$apollo.query({
                    query: ProblemListGQL,
                    variables:{
                        page: this.page
                    },
                }).then( response => response.data.problemList )
                   .then( data => { this.problemItem = data.problemList , this.maxpage = data.maxpage } )
                   .then( () => this.isLoading = false )
            },
            resolve: function( index ){
                return () => this.request( index );
            }
        }
    }
</script>
