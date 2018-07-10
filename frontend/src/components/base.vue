<template>
    <div>
        <Navbar/>

        <div id = 'main-container'>
            <router-view></router-view>
            <Footer/>
        </div>
    </div>
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
