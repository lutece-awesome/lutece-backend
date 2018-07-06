<template>
    <div class="ui pagination menu">

    </div>
</template>

<script>
    export default {
        props:{
            maxpage:{
                type: Number,
                required: true
            },
            current:{
                type: Number,
                required: true
            },
            count:{
                type: Number,
                default: 10
            }
        },
        created(){

        },
        data: function(){
            return{
                _rangel : 0,
                _ranger : 0
            }
        }
    }
</script>
