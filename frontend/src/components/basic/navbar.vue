<!--
    Navigation Bar
-->
<template>
    <div class = 'ui fixed top borderless large menu'>
        <div class = 'ui container'>
            <div class="header item">Lutece</div>
            <router-link to="/home" class = 'item' active-class = 'active'  >Home</router-link>
            <router-link :to="{ name: 'ProblemList' , params: { page: 1 } }" class = 'item' active-class = 'active' > Problem </router-link>
        </div>
        <div class="right menu">

            <div v-if = 'userAuthed' class = 'item'>
                <img :src = gravataremail alt="" />
                <div style = 'margin-left: 10px;' ><a href = "" style = "color:black" >{{ displayname }}</a></div>
            </div>

            <div class="item">
                <FormButton v-bind:class= '{ loading: logging , disabled: logging }' v-if='!userAuthed' buttonstyle = 'ui primary button' icon = 'sign in icon' msg = 'Sign in' :resolve = 'login'  />
                <FormButton v-else buttonstyle = 'ui negative button' icon = 'sign out icon' msg = 'Sign out' :resolve = 'signout'  />
            </div>
        </div>
    </div>
</template>

<script>
    import FormButton from '@/components/basic/formbutton.vue'
    import { verifyToken , refreshToken } from '@/graphql/basic/token.js'
    export default {
        data: function(){
            return {
                userAuthed: false,
                gravataremail: '',
                displayname: '',
                logging: false
            }
        },
        components:{
            FormButton
        },
        created(){
            this.refresh();
            this.$bus.on( 'navbarUserRefresh' , this.refresh );
        },
        methods:{
            refresh: function(){
                this.userAuthed = false;
                this.logging = true;
                this.$apollo.mutate({
                    mutation: verifyToken,
                    variables:{
                        token: localStorage.getItem('USER_TOKEN') || ''
                    }})
                    .then( response => response.data.verifyToken.payload )
                    .then( data => {
                        this.displayname = data.displayname;
                        this.gravataremail = data.gravataremail;
                        this.userAuthed = true;
                        this.logging = false;
                        // console.log( data );
                    })
                    .catch( error => {this.userAuthed = false; this.logging = false; } );
            },
            login: function(){
                this.$router.push( { name : 'Login' } );
            },
            signout: function(){
                localStorage.removeItem( 'USER_TOKEN' );
                this.refresh();
            }
        }
    }
</script>