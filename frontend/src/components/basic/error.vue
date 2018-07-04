<template>
    <div v-bind:class = 'errorstyle' >
        <div class = 'header'> {{ header }} </div>
        <ul v-if = 'msg' class = 'list'>
            <li> {{ msg }} </li>
        </ul>
    </div>
</template>

<script>
    export default {
        props:{
            errorstyle : {
                type : String,
                default : 'ui compact negative message'
            },
            header :{
                type: String,
                default : 'Some errors occured, Please refresh.',
            },
            msg : {
                type: String,
                default : ''
            }
        }
    }
</script>
