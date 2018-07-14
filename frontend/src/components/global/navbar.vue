<template>
    <div>
        <v-navigation-drawer v-model="drawer" fixed clipped app :width="240">
            <v-list>
                <v-list-tile v-for="item in items" :key="item.title" :to="item.path" ripple active-class="grey lighten-2">
                    <v-list-tile-action>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
            </v-list>
        </v-navigation-drawer>
        <v-toolbar fixed clipped-left app dark color="primary">
            <v-toolbar-side-icon @click.stop="drawer=!drawer"></v-toolbar-side-icon>
            <v-toolbar-title>
                Lutece
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items class="hidden-sm-and-down">
                <v-btn flat v-if='!logging && !authed' @click='login'>
                    <v-icon class='mr-2'>mdi-login</v-icon>
                    SIGN IN
                </v-btn>
                <v-menu v-if='authed' open-on-hover offset-y>
                    <v-btn slot="activator" flat>
                        <v-avatar v-if='authed' size='36' class="mr-2" >
                            <img :src=gravataremail />
                        </v-avatar>
                        {{ displayname }}
                        <v-icon>mdi-menu-down</v-icon>
                    </v-btn>
                    <v-list>
                        <v-list-tile @click='signout'>
                            <v-icon class='mr-2'>mdi-logout</v-icon>
                            <v-list-tile-content>
                                <v-list-tile-title>Sign Out</v-list-tile-title>
                            </v-list-tile-content>
                        </v-list-tile>
                    </v-list>
                </v-menu>
            </v-toolbar-items>
            <v-btn icon v-if='authed' class="hidden-md-and-up">
                <v-avatar size='36'>
                    <img :src=gravataremail />
                </v-avatar>
            </v-btn>
            <v-btn icon v-if='authed' @click='signout' class="hidden-md-and-up">
                <v-icon>mdi-logout</v-icon>
            </v-btn>
            <v-btn icon v-if='!logging && !authed' @click='login' class="hidden-md-and-up">
                <v-icon>mdi-login</v-icon>
            </v-btn>
        </v-toolbar>
    </div>
</template>

<script>
    import Login from "@/components/signin/login.vue";
    import {
        verifyToken,
        refreshToken
    } from "@/graphql/signin/token.js";
    export default {
        data: function() {
            return {
                drawer: null,
                signin: false,
                logging: true,
                items: [{
                        icon: 'mdi-home',
                        title: 'Home',
                        path: '/home'
                    },
                    {
                        icon: 'mdi-view-list',
                        title: 'Problem',
                        path: '/problemlist'
                    },
                    {
                        icon: 'mdi-chart-bar',
                        title: 'Status',
                        path: ''
                    },
                    {
                        icon: 'mdi-trophy',
                        title: 'Contest',
                        path: ''
                    },
                    {
                        icon: 'mdi-account-multiple',
                        title: 'User',
                        path: ''
                    },
                    {
                        icon: 'mdi-information',
                        title: 'About',
                        path: ''
                    },
                ]
            };
        },
        components: {
            Login
        },
        mounted() {
            this.refresh();
        },
        watch: {
            authed: function() {
                this.refresh();
            }
        },
        computed: {
            authed: function() {
                return this.$store.state["user"].authed;
            },
            gravataremail: function() {
                return this.$store.state["user"].gravataremail;
            },
            displayname: function() {
                return this.$store.state["user"].displayname;
            }
        },
        methods: {
            refresh() {
                this.logging = true;
                this.$apollo
                    .mutate({
                        mutation: verifyToken,
                        variables: {
                            token: localStorage.getItem("USER_TOKEN") || ""
                        }
                    })
                    .then(response => response.data.verifyToken.payload)
                    .then(data => {
                        this.$store.commit("user/update_authed", true);
                        this.$store.commit("user/update_gravataremail", data.gravataremail);
                        this.$store.commit("user/update_displayname", data.displayname);
                        this.logging = false;
                    })
                    .catch(error => {
                        this.logging = false;
                    });
            },
            login: function() {
                this.$router.push({
                    name: "Login",
                    query: {
                        redirect: this.$route.path
                    }
                });
            },
            signout: function() {
                this.$router.push({
                    name: "Signout",
                    query: {
                        redirect: this.$route.path
                    }
                });
            }
        }
    };
</script>
