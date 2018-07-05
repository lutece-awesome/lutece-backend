<template>
    <div v-bind:class = "[stateclass , buttonstyle ]" @click = "clickaction" >
        <i v-if = 'icon' v-bind:class = 'icon'></i>
        {{ msg }}
    </div>
</template>

<script>
    // action shoule be promise
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
            resolve: {
                type : Function,
                default : () => {}
            },
            action : {
                type: Function,
                default : () => new Promise( function( resolve , reject ){ resolve() } )
            },
            error : {
                type: Function,
                default : () => {}
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
                this.action()
                    .then( data => { this.resolve( data ) , this.isLoading = false } )
                    .catch( error => { this.isLoading = false , this.isError = true , this.error( error ) } )
            }
            
        }

    }
</script>