<template>
    <div v-bind:class = "[stateclass , buttonstyle ]" @click = "_clickaction" >
        <i v-if = 'icon' v-bind:class = 'icon'></i>
        {{ msg }} 
    </div>
</template>

<script>
    export default {
        props: {
            msg : String,
            buttonstyle : String,
            icon : String,
            clickaction : Function
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

            _clickaction: function(){
                try{
                    this.clickaction();
                }catch( s ){

                }
            }
        }

    }
</script>