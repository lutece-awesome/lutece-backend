
<template>
    <v-layout justify-center>
        <v-flex xs12 sm8 md6 xl4>
            <v-card>
                <v-card-title>
                    <v-layout justify-center mt-3>
                        <span class="headline">SIGN UP</span>
                    </v-layout>
                </v-card-title>
                <v-card-text>
                    <form>
                        <v-layout column>
                            <v-flex>
                                <v-text-field v-model="username" label="Username *" :error-messages="geterror('username')" required />
                            </v-flex>
                            <v-flex>
                                <v-text-field v-model="password" type="password" label="Password *" :error-messages="geterror('password')" required />
                            </v-flex>
                            <v-flex>
                                <v-text-field v-model="email" label="Email *" :error-messages="geterror('email')" required />
                            </v-flex>
                            <v-flex>
                                <v-text-field v-model="displayname" label="Display name *" :error-messages="geterror('displayname')" required />
                            </v-flex>
                            <v-flex>
                                <v-text-field v-model="school" :error-messages="geterror('school')" label="School" />
                            </v-flex>
                            <v-flex>
                                <v-text-field v-model="company" :error-messages="geterror('company')" label="Company" />
                            </v-flex>
                            <v-flex>
                                <v-text-field v-model="location" :error-messages="geterror('location')" label="Location" />
                            </v-flex>
                            <v-flex mt-3>
                                <v-btn block big v-bind:loading=loading @click='register' :color='error ? "error" : "primary"'>Register</v-btn>
                            </v-flex>
                        </v-layout>
                    </form>
                </v-card-text>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
    import {
        RegisterGQL
    } from '@/graphql/signin/register.js'
    export default {
        data: function() {
            return {
                username: '',
                password: '',
                email: '',
                displayname: '',
                school: '',
                company: '',
                location: '',
                loading: false,
                error: false,
                errordetail: {},
            }
        },
    
        methods: {
    
            geterror: function(field) {
                if (this.errordetail.hasOwnProperty(field))
                    return this.errordetail[field][0].message;
                return ''
            },
    
            register: function() {
                this.errordetail = {};
                this.error = false;
                this.loading = true;
                this.$apollo.mutate({
                        mutation: RegisterGQL,
                        variables: {
                            username: this.username,
                            password: this.password,
                            email: this.email,
                            displayname: this.displayname,
                            school: this.school,
                            company: this.company,
                            location: this.location
                        }
                    })
                    .then(response => response.data.Register)
                    .then(data => {
                        this.aftersignup(data.token, data.payload);
                    })
                    .catch(error => {
                        this.error = true;
                        this.errordetail = JSON.parse(error.graphQLErrors[0].message);
                    })
                    .finally(() => (this.loading = false))
            },
    
            aftersignup: function(token, payload) {
                let s = JSON.parse(payload)
                Object.values(this.$apollo.provider.clients)
                    .forEach(client => client.cache.reset())
                localStorage.setItem('USER_TOKEN', token);
                this.$store.commit('user/update_authed', true);
                // this.$store.commit("user/update_gravataremail", data.gravataremail);
                // this.$store.commit("user/update_displayname", data.displayname);
                this.$router.push({
                    name: 'Home'
                });
            }
        }
    }
</script>
