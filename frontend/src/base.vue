<template>
    <v-app>
        <Navbar/>
        <Toolbar/>
        <v-content>
            <v-container fluid>
                <router-view></router-view>
            </v-container>
        </v-content>
    </v-app>
</template>


<script>
    import Toolbar from '@/components/global/toolbar.vue'
    import Footer from '@/components/global/footer.vue'
    import Navbar from '@/components/global/navbar.vue'
    export default {
        components:{
            Toolbar,
            Navbar,
            Footer
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
