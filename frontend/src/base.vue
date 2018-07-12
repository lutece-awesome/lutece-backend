<template>
    <v-app>
        <Navbar/>
        <v-content>
            <v-container fluid>
                <router-view></router-view>
            </v-container>
        </v-content>
    </v-app>
</template>


<script>
    import Footer from "@/components/global/footer.vue";
    import Navbar from "@/components/global/navbar.vue";
    export default {
        components: {
            Navbar,
            Footer
        }
    };
</script>

<style>
    .v-label.error--text {
        animation: none !important;
    }
</style>
