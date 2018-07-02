<template>
    <div>
        <navbar/>
        <div id = 'main-container'>
            <router-view></router-view>
        </div>
    </div>
</template>


<script>
    import navbar from './basic/navbar.vue'
    export default {
        components:{
            navbar,
        }
    }
</script>

<style scoped>
    #main-container{
        padding-top: 80px;
        padding-left: 225px;
        padding-right: 225px; 
    }    
</style>
