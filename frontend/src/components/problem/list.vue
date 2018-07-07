<template>
    <div>
        <Loading v-if = "isLoading" loadingstyle = 'ui indeterminate text loader' v-bind:isLoading = 'isLoading' />
        <div v-else>
            <Paginator v-bind:maxpage = parseInt(maxpage) v-bind:page = parseInt(page) />
            <table class = "ui padded table" style = 'text-align:center' >
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Accepted / Submit</th>
                    <th>Ratio</th>        
                </tr>
                <tr v-for= "each in problemItem" :key = 'each.problemId' >
                    <td> {{ each.problemId }} </td>
                    <td> {{ each.title }} </td>
                    <td> {{ each.accept }} / {{ each.submit }} </td>
                    <td> {{ each.submit ? ( ( each.accept / each.submit ) * 100 ).toFixed( 2 ) : '0.00' }}% </td>
                </tr>
            </table>
        </div>
    </div>
</template>


<script>
    import Loading from '@/components/basic/loading.vue'
    import Paginator from '@/components/basic/paginator.vue'
    import { ProblemList } from '@/graphql/problem/list.js'
    export default {

        components:{
            Loading,
            Paginator
        },

        props:{
            page:{
                type: String,
                required: true
            }
        },

        data(){
            return{
                isLoading: true,
                maxpage: 0,
                problemItem : [],
            }
        },

        mounted(){
            let maxpage = 1
            this.$apollo.query({
                query: ProblemList,
                variables:{
                    page: parseInt( this.page )
                },
            }).then( response => response.data.problemList )
              .then( data => { this.problemItem = data.problemList , this.maxpage = data.maxpage } )
              .then( () => this.isLoading = false )
            console.log( this.maxpage );
        },

    }
</script>

