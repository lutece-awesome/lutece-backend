<template>
    <v-autocomplete 
        v-model = "model"
        :items = "items"
        :loading = "isLoading"
        :search-input.sync = "search"
    >
    </v-autocomplete>
</template>


<script>
    export default {
        data: function(){
            return{
                model: null,
            }
        }
    }

</script>

