<template>
    <div>
        <Loading v-if = "isLoading" loadingstyle = 'ui indeterminate text loader' v-bind:isLoading = 'isLoading' />
        <div v-else>
            <div class="ui two column stackable grid">
                <div class = 'left floated column' >
                    <Paginator v-bind:maxpage = parseInt(maxpage) v-bind:page = parseInt(page) v-bind:resolve = resolve />
                </div>

                <div class = 'column'>
                    <div class="ui search" style = 'float:right;' >
                        <div class="ui icon input">
                            <input class="prompt" type="text" placeholder="通用密码">
                            <i class="search icon"></i>
                        </div>
                        <div class="results"></div>
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
    import { ProblemListGQL } from '@/graphql/problem/list.js'
    export default {

        components:{
            Paginator,
            ProblemList,
            Loading
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
                this.page = page;
                this.isLoading = true;
                this.$apollo.query({
                    query: ProblemListGQL,
                    variables:{
                        page: parseInt( this.page )
                    },
                }).then( response => response.data.problemList )
                   .then( data => { this.problemItem = data.problemList , this.maxpage = data.maxpage , this.page = Math.min( this.page , this.maxpage  ) } )
                   .then( () => this.isLoading = false )
            },
            resolve: function( index ){
                return () => this.request( index );
            }
        }
    }
</script>
