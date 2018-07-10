<template>
    <v-app>
        <Navbar/>
        <v-content>
            <v-container fluid>
                <router-view></router-view>
            </v-container>
        </v-content>
        <v-footer app></v-footer>
    </v-app>
</template>


<script>
    import Navbar from '@/components/global/navbar.vue'
    import Footer from '@/components/global/footer.vue'
    export default {
        components:{
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
