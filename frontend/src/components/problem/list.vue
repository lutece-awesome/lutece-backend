<template>
    <div>
        
    </div>
</template>


<script>
    import { ProblemList } from '@/graphql/problem/list.js'
    export default {
        data: function(){
            return{
                problemItem : []
            }
        },

        created(){

        },

        apollo:{
            problemItem:{
                query: ProblemList,
                variables:{
                    page: 1
                }
            }
        }
    }
</script>

