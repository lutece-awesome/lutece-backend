<template>
    <div v-if= "isLoading" class="ui segment" v-bind:style = "{ height: height + 'px'}" >
        <div class="ui active inverted dimmer">
            <div v-bind:class= loadingstyle >{{ loadingmsg }}</div>
        </div>
    </div>
</template>

<script>
    export default {
        props:{
            height:{
                type: Number,
                default : 250
            },
            loadingmsg:{
                type: String,
                default : 'Loading'
            },
            loadingstyle:{
                type: String,
                default: 'ui text loader'
            }
        },
        data: function(){
            return {
                isLoading: true
            }
        }
    }
</script>
