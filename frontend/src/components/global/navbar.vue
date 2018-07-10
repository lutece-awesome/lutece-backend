<!--
    Navigation Bar
-->
<template>
    <v-toolbar>
        <v-toolbar-side-icon></v-toolbar-side-icon>
        <v-toolbar-title>Lutece</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-sm-and-down">
            <v-btn flat> SIGN IN </v-btn>
        </v-toolbar-items>
        <!-- <div class = 'ui container'>
            <div class="header item">Lutece</div>
            <router-link to = "/home" class = 'item' active-class = 'active'  >Home</router-link>
            <router-link to = "/problemlist" class = 'item' active-class = 'active' > Problem </router-link>
        </div>
        <div class="right menu">

            <div v-if = 'authed' class = 'item'>
                <img :src = gravataremail alt="" />
                <div style = 'margin-left: 10px;' ><a href = "" style = "color:black" >{{ displayname }}</a></div>
            </div>

            <div class="item">
                <FormButton v-bind:class= '{ loading: logging , disabled: logging }' v-if='!authed' buttonstyle = 'ui primary button' icon = 'sign in icon' msg = 'Sign in' :resolve = 'login'  />
                <FormButton v-else buttonstyle = 'ui negative button' icon = 'sign out icon' msg = 'Sign out' :resolve = 'signout'  />
            </div>
        </div> -->
    </v-toolbar>
</template>

<script>
    import { mapGetters } from 'vuex'
    import FormButton from '@/components/basic/formbutton.vue'
    import { verifyToken , refreshToken } from '@/graphql/signin/token.js'
    export default {
        data: function(){
            return {
                logging: false
            }
        },
        components:{
            FormButton
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
            displayname: function(){
                return this.$store.state['user'].displayname;
            },
            gravataremail: function(){
                return this.$store.state['user'].gravataremail;
            }
        },
        methods:{
            login: function(){
                this.$router.push( { name : 'Login' , query:{ redirect: this.$route.path } } );
            },
            signout: function(){
                this.$router.push( { name : 'Signout' , query:{ redirect: this.$route.path } } );
            }
        }
    }
</script>