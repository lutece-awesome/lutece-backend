<template>
    <div class="ui search">
        <div class="ui icon input">
            <input class = "prompt" type="text" v-bind:placeholder = placeholder >
            <i class="search icon" ></i>
        </div>
        <div class="results"></div>
    </div>
</template>


<script>
    export default {
        props:{
            placeholder:{
                type: String,
                default: ''
            },
        }
    }
</script>
