<!--
    Navigation Bar
-->
<template>
    <div class = 'ui fixed top borderless large menu'>
        <div class = 'ui container'>
            <div class="header item">Lutece</div>
            <router-link to="/home" class = 'item' active-class = 'active'  >Home</router-link>
            <router-link to='/problem' class = 'item' active-class = 'active' > Problem </router-link>
        </div>
        <div class="right menu">
            <div class="item">
                <FormButton v-if='!userAuthed' buttonstyle = 'ui primary button' icon = 'sign in icon' msg = 'Sign in' :resolve = 'login'  />
                <FormButton v-else buttonstyle = 'ui negative button' icon = 'sign out icon' msg = 'Sign out' :resolve = 'signout'  />
            </div>
        </div>
    </div>
</template>

<script>
    import FormButton from '@/components/basic/formbutton.vue'
    import { UserAuthedGQL } from '@/graphql/basic/authcheck.js'
    export default {
        data: () => {
            return {
                UserAuthed: false
            }
        },
        components:{
            FormButton
        },
        apollo:{
            userAuthed:{
                query: UserAuthedGQL
            }
        },
        methods:{
            login: function(){
                this.$router.push( { name : 'Login' } );
            },
            signout: function(){
                alert( "3231" );
            }
        }
    }
</script>