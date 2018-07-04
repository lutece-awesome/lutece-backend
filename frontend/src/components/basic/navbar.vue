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
                <FormButton v-if='!authed' buttonstyle = 'ui primary button' icon = 'sign in icon' msg = 'Sign in' :action = 'login'  />
                <FormButton v-else buttonstyle = 'ui negative button' icon = 'sign out icon' msg = 'Sign out' :action = 'signout'  />
            </div>
        </div>
    </div>
</template>

<script>
    import FormButton from '@/components/basic/formbutton.vue'
    export default {
        data: function(){
            return {
                authed: false
            }
        },
        components:{
            FormButton
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