<template>
  <div>
      <v-navigation-drawer v-model="drawer" fixed clipped app>
        <v-list>

          <v-list-tile to = 'Home' >
            <v-list-tile-action>
              <v-icon>fa-home</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Home</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile>
            <v-list-tile-action>
              <v-icon>fa-tasks</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Problem</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile>
            <v-list-tile-action>
              <v-icon>fa-chart-bar</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Status</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile>
            <v-list-tile-action>
              <v-icon>fa-trophy</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Contest</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile>
            <v-list-tile-action>
              <v-icon>fa-user</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>User</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile>
            <v-list-tile-action>
              <v-icon>fa-compass</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>About</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

        </v-list>
      </v-navigation-drawer>

      <v-toolbar fixed clipped-left app dark  class="primary">

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

          <v-avatar v-if = 'authed' >
            <img :src = gravataremail />
          </v-avatar>
          
          <v-menu v-if = 'authed' open-on-hover offset-x offset-y> 
              
            <v-btn slot = "activator" flat> 
                {{ displayname }} 
                <v-icon right>fa-caret-down</v-icon>
            </v-btn>

            <v-list>

              <v-list-tile @click = 'signout'>

                <v-list-tile-action>
                  <v-icon>fa-sign-out-alt</v-icon>
                </v-list-tile-action>

                <v-list-tile-content>
                  <v-list-tile-title > Sign Out </v-list-tile-title>
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
    import { verifyToken, refreshToken } from "@/graphql/signin/token.js";
    export default {
        data: function() {
            return {
                drawer: false,
                signin: false,
                logging: true,
            };
        },
        components: {
          Login
        },
        mounted() {
          this.refresh();
        },
        watch:{
          authed: function(){
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
          displayname: function(){
              return this.$store.state["user"].displayname;
          }
        },
        methods: {
          refresh(){
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
              query: { redirect: this.$route.path }
            });
          },
          signout: function() {
            this.$router.push({
              name: "Signout",
              query: { redirect: this.$route.path }
          });
        }
      }
  };
</script>
