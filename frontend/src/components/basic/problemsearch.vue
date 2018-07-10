<template>


    <div class="ui search">
        <div class="ui left icon input">
            <i class="search icon" ></i>
            <input class = "prompt" type="text" v-bind:placeholder = placeholder >
        </div>
        <div class="results transition visible" >
            <div class = 'content'>
                <div class = 'menu'>
                    <div class = 'title search item' ><b> A PLUS B </b></div>
                    <div class = 'title search item' ><b> A PLUS B </b></div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
    export default {
        props:{
            placeholder:{
                type: String,
                default: ''
            },
        },
        created(){

        }
    }

</script>

<style scoped>
    .search.item{
        overflow: hidden;
        margin-left: 10px;
        margin-top: 8px;
        margin-bottom: 8px;
        font-weight: 500;
        font-size: 1em;
        color: rgba(0,0,0,.85);
    }
</style>

