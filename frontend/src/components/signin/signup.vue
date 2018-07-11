
<template>
    <v-card style = 'width:600px; margin-top:32px; margin-left:auto; margin-right:auto;' >
        <v-card-title>
            <span class = 'headline' style = 'margin:0 auto;'>
                SIGN UP
            </span>
        </v-card-title>
        <v-card-text>
            <v-container grid-list-md>
                <v-form>
                    <v-layout row wrap>
                        <v-flex xs12>
                            <v-text-field v-model = "username" label = "Username *" required :error-messages = "geterror('username')" />
                        </v-flex>
                        <v-flex xs12>
                            <v-text-field v-model = "password" type = "password" label = "Password *" :error-messages = "geterror('password')" required />
                        </v-flex>
                        <v-flex xs12>
                            <v-text-field v-model = "email" label = "Email *" :error-messages = "geterror('email')" required />
                        </v-flex>
                        <v-flex xs12>
                            <v-text-field v-model = "displayname" label = "Display name *" :error-messages = "geterror('displayname')" required />
                        </v-flex>
                        <v-flex xs12>
                            <v-text-field v-model = "school" :error-messages = "geterror('school')" label = "School"/>
                        </v-flex>
                        <v-flex xs12>
                            <v-text-field v-model = "company" :error-messages = "geterror('company')" label = "Company"/>
                        </v-flex>
                        <v-flex xs12>
                            <v-text-field v-model = "location" :error-messages = "geterror('location')" label = "Location"/>
                        </v-flex>
                        <v-flex xs12>
                            <v-btn block big v-bind:loading = loading @click = 'register' :color = 'error ? "error" : "primary"'  >Register</v-btn>
                        </v-flex>
                    </v-layout>
                </v-form>
            </v-container>
        </v-card-text>
    </v-card>
</template>

<script>
    import { RegisterGQL } from '@/graphql/signin/register.js'
    export default {
        data: function(){
            return {
                username : '',
                password : '',
                email : '',
                displayname : '',
                school : '',
                company : '',
                location : '',
                loading: false,
                error: false,
                errordetail: {},
            }
        },
        
        methods:{

            geterror: function( field ){
                if(this.errordetail.hasOwnProperty( field ))
                    return this.errordetail[field][0].message;
                return ''
            },

            register: function(){
                this.errordetail = {};
                this.error = false;
                this.loading = true;
                this.$apollo.mutate({
                    mutation: RegisterGQL,
                    variables:{
                        username: this.username,
                        password: this.password,
                        email: this.email,
                        displayname: this.displayname,
                        school: this.school,
                        company: this.company,
                        location: this.location
                    }
                })
                .then( response => response.data.Register )
                .then( data => {
                    this.loading = false;
                    this.aftersignup( data.token , data.payload );
                })
                .catch( error => {
                    this.loading = false;
                    this.error = true;
                    this.errordetail = JSON.parse( error.graphQLErrors[0].message );
                })
            },

            aftersignup: function( token , payload ){
                let s = JSON.parse( payload )
                localStorage.setItem('USER_TOKEN', token );
                this.$store.commit( 'user/update_authed' , true );
                console.log( s );
            }
        }
    }
</script>
