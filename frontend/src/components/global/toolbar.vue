<!--
    Navigation Bar
-->
<template>
    <v-toolbar :clipped-left = "$vuetify.breakpoint.lgAndUp" fixed app>
        <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
            <v-toolbar-side-icon />
            <span class="hidden-sm-and-down">Lutece</span>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items v-if = '!logging' class="hidden-sm-and-down">
            <v-btn @click = 'login' flat>
                <v-icon left>fa-sign-in-alt</v-icon>
                SIGN IN
            </v-btn>
        </v-toolbar-items>
    </v-toolbar>
</template>

<script>
    import { mapGetters } from 'vuex'
    import Login from '@/components/signin/login.vue'
    import { verifyToken , refreshToken } from '@/graphql/signin/token.js'
    export default {
        data: function(){
            return {
                signin: false,
                logging: true
            }
        },
        components:{
            Login
        },
        mounted(){
            this.userAuthed = false;
            this.logging = true;
            this.$apollo.mutate({
                mutation: verifyToken,
                variables:{
                    token: localStorage.getItem('USER_TOKEN') || ''
                }})
                .then( response => response.data.verifyToken.payload )
                .then( data => {
                    this.$store.commit( 'user/update_authed' , true );
                    this.$store.commit( 'user/update_gravataremail' , data.gravataremail );
                    this.$store.commit( 'user/update_displayname' , data.displayname );
                    this.logging = false;
                })
                .catch( error => { this.logging = false; } );
        },
        computed:{
            authed: function(){
                return this.$store.state['user'].authed;
            },
            gravataremail: function(){
                return this.$store.state['user'].gravataremail;
            }
        },
        methods:{
            login: function(){
                this.$router.push( { name : 'Login' , query:{ redirect: this.$route.path } } );
            },
            signup: function(){
                
            },
            signout: function(){
                this.$router.push( { name : 'Signout' , query:{ redirect: this.$route.path } } );
            }
        }
    }
</script>