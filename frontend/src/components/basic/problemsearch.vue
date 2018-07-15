<template>
    <v-autocomplete 
        v-model = "model"
        :items = "items"
        :loading = "isLoading"
        :search-input.sync = "search"
        hide-no-data        
        append-icon = ''
        prepend-icon="mdi-magnify"
        return-object
    >
    </v-autocomplete>
</template>


<script>
    export default {
        data: function(){
            return{
                model: null,
                result: [],
                isLoading: false,
                search: null,
            }
        },

        watch:{
            search( val ){
                if( val.length == 0 || this.isLoading ) return;
                this.isLoading = true;
                this.$apollo.query({
                    query: ProblemListGQL,
                    variables: {
                        page: this.page
                    },
                })
            }
        }
        

    }

</script>

