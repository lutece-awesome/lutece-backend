<template>
    <div v-bind:class = "[stateclass , buttonstyle ]" v-on:click = "action" >
        {{ msg }} 
    </div>
</template>

<script>
    export default {
        props: [ 'msg' , 'buttonstyle' , 'request' ],
        data: function(){
            return　{
                isLoading: false,
                isError : false,
            }
        },
        computed:{
            stateclass: function(){
                return {
                    loading: this.isLoading,
                    disabled : this.isLoading,
                    negative : this.isError,
                }
            },

        },
        methods:{
            action: function(){
                this.isLoading = true;
                this.isError = false;
                
            }
        }
    }
</script>