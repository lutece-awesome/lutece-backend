<template>
    <div>
        <v-card style = 'width:600px; margin-top:128px; margin-left:auto; margin-right:auto;' >
            <v-card-title>
                <span class = 'headline' style = 'margin:0 auto;'>
                    SIGN IN
                </span>
            </v-card-title>
            <v-card-text>
                <v-container grid-list-md>
                    <v-form>
                        <v-layout row wrap>
                            <v-flex xs12>
                                <v-text-field v-model = "username" label = "Username" required />
                            </v-flex>
                            <v-flex xs12>
                                <v-text-field v-model = "password" type = "password" label = "Password" required />
                            </v-flex>
                            <v-flex xs12 sm6>
                                <a @click = 'signup' >Do not have account? </a>
                            </v-flex>
                            <v-flex xs12>
                                <v-btn block big :loading = loading @click = 'login' :color = 'error ? "error" : "primary"'  >Login</v-btn>
                            </v-flex>
                        </v-layout>
                    </v-form>
                </v-container>
            </v-card-text>
        </v-card>
        <v-alert :value = error type = 'error' style = 'margin:0;' > {{ errormsg }} </v-alert>
    </div>
</template>


<script>
    import { tokenAuth } from '@/graphql/signin/token.js'
    export default {

        data: () => ({
            loading: false,
            error: false,
            username : '',
            password : '',
            errormsg : '',
        }),

        methods:{
            login: function(){
                this.loading = true;
                this.error = false;
                this.$apollo.mutate({
                    mutation: tokenAuth,
                    variables:{
                        username: this.username,
                        password: this.password
                    },
                })
                .then( response => response.data.tokenAuth )
                .then( data => {
                    localStorage.setItem('USER_TOKEN', data.token );
                    this.$store.commit( 'user/update_authed' , true );
                    this.loading = false;
                    this.dialog = false;
                    location.reload();
                })
                .catch( error => {
                    this.errormsg = String( error );
                    this.error = true;
                    this.loading = false;
                })
            },
            redirect: function(){
                Object.values(this.$apollo.provider.clients)
                    .forEach(client => client.cache.reset())
                this.$router.push (this.$route.query.redirect || '/' );
            },
            signup: function(){
                
            },
        }
    }
</script>