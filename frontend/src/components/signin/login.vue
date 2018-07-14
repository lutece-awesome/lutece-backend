<template>
    <v-layout justify-center>
        <v-flex xs12 sm6 md4>
            <v-card>
                <v-card-title>
                    <v-layout justify-center mt-3>
                        <span class="headline">SIGN IN</span>
                    </v-layout>
                </v-card-title>
                <v-card-text>
                    <form>
                        <v-layout column>
                            <v-flex>
                                <v-text-field v-model="username" label="Username" :error-messages="geterror('username')" required />
                            </v-flex>
                            <v-flex>
                                <v-text-field v-model="password" type="password" label="Password" :error-messages="geterror('password')" required />
                            </v-flex>
                            <v-flex>
                                <a @click='signup'>Do not have account? </a>
                            </v-flex>
                            <v-flex class="text-xs-center" mt-3>
                                <v-btn block big :loading=loading @click='login' :color='error ? "error" : "primary"'>Login</v-btn>
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
        UserLogin
    } from "@/graphql/signin/token.js";
    export default {
        data: () => ({
            loading: false,
            error: false,
            username: "",
            password: "",
            errordetail: {}
        }),
    
        methods: {

            geterror: function(field) {
                if (this.errordetail.hasOwnProperty(field))
                    return this.errordetail[field][0].message;
                return ''
            },

            login: function() {
                this.loading = true;
                this.error = false;
                this.errordetail = {};
                this.$apollo
                    .mutate({
                        mutation: UserLogin,
                        variables: {
                            username: this.username,
                            password: this.password
                        }
                    })
                    .then(response => response.data.UserLogin)
                    .then(data => {
                        localStorage.setItem("USER_TOKEN", data.token);
                        this.$store.commit("user/update_authed", true);
                        this.loading = false;
                        this.redirect();
                    })
                    .catch(error => {
                        this.errordetail = JSON.parse(error.graphQLErrors[0].message);
                        this.error = true;
                        this.loading = false;
                    });
            },

            redirect: function() {
                Object.values(this.$apollo.provider.clients).forEach(client =>
                    client.cache.reset()
                );
                this.$router.push(this.$route.query.redirect || "/");
            },
            
            signup: function() {
                this.$router.push({
                    name: "Signup"
                });
            }
        }
    };
</script>