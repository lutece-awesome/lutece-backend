<template>
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
</template>


<script>
    import { ProblemList } from '@/graphql/problem/list.js'
    export default {

        data(){
            return{
                problemItem : [],
            }
        },

        created(){
            this.$apollo.query({
                query: ProblemList,
                variables:{
                    page: 1
                },
            }).then( response => response.data.problemList )
              .then( data => this.problemItem = data )
        },

    }
</script>

