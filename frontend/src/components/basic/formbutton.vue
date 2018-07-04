<template>
    <div v-bind:class = "[stateclass , buttonstyle ]" @click = "clickaction" >
        <i v-if = 'icon' v-bind:class = 'icon'></i>
        {{ msg }}
    </div>
</template>

<script>
    export default {
        props: {
            msg :{
                type : String,
                default : ''
            },
            buttonstyle : {
                type: String,
                default : 'ui primary button'
            },
            icon: String,
            action : {
                type: Function,
                default : function(){}
            },
            error : {
                type: Function,
                default : function(){}
            }
        },
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

            clickaction: async function(){
                this.isLoading = true;
                this.isError = false;
                try{
                    this.action();
                    this.isLoading = false;
                }catch( error ){
                    this.isLoading = false;
                    this.isError = true;
                    this.error( error );
                }
            }
            
        }

    }
</script>