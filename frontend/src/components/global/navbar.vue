<template>
    <div>
        <v-navigation-drawer v-model="drawer" fixed clipped app>
            <v-list>
                <v-list-tile v-for="item in items" :key="item.title" :to="item.path" ripple>
                    <v-list-tile-action>
                        <v-icon class="fa-fw">{{ item.icon }}</v-icon>
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
                    <v-icon left>fa-sign-in-alt</v-icon>
                    SIGN IN
                </v-btn>
            </v-toolbar-items>
            <v-avatar v-if='authed'>
                <img :src=g ravataremail />
            </v-avatar>
            <v-menu v-if='authed' open-on-hover offset-x offset-y>
                <v-btn slot="activator" flat>
                    {{ displayname }}
                    <v-icon right>fa-caret-down</v-icon>
                </v-btn>
                <v-list>
                    <v-list-tile @click='signout'>
                        <v-list-tile-action>
                            <v-icon>fa-sign-out-alt</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title> Sign Out </v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </v-list>
            </v-menu>
            <v-btn icon v-if='!logging && !authed' @click='login' class="hidden-md-and-up">
                <v-icon>fa-sign-in-alt</v-icon>
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
                        icon: 'fa-home',
                        title: 'Home',
                        path: '/home'
                    },
                    {
                        icon: 'fa-tasks',
                        title: 'Problem',
                        path: ''
                    },
                    {
                        icon: 'fa-chart-bar',
                        title: 'Status',
                        path: ''
                    },
                    {
                        icon: 'fa-trophy',
                        title: 'Contest',
                        path: ''
                    },
                    {
                        icon: 'fa-user',
                        title: 'User',
                        path: ''
                    },
                    {
                        icon: 'fa-compass',
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
