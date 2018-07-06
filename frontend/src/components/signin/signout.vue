<template>
    
</template>


<script>
    export default {
        created(){
            Object.values(this.$apollo.provider.clients)
                .forEach(client => client.cache.reset())
            localStorage.removeItem( 'USER_TOKEN' );
            this.$router.push (this.$route.query.redirect || '/' );
        }
    }
</script>
