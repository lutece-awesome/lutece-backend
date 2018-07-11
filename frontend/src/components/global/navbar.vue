<template>
<div>
    <v-navigation-drawer v-model="drawer" fixed clipped app>
      <v-list>

        <v-list-tile @click="">
          <v-list-tile-action>
            <v-icon>fa-home</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Home</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile @click="">
          <v-list-tile-action>
            <v-icon>fa-tasks</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Problem</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile @click="">
          <v-list-tile-action>
            <v-icon>fa-chart-bar</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Status</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile @click="">
          <v-list-tile-action>
            <v-icon>fa-trophy</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>Contest</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile @click="">
          <v-list-tile-action>
            <v-icon>fa-user</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>User</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile @click="">
          <v-list-tile-action>
            <v-icon>fa-compass</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>About</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

      </v-list>
    </v-navigation-drawer>
    <v-toolbar fixed clipped-left app dark class="primary">
        <v-toolbar-side-icon @click.stop="drawer=!drawer"></v-toolbar-side-icon>
        <v-toolbar-title>
            Lutece
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-sm-and-down">
            <v-btn flat v-if='!logging' @click='login'>
                <span class="mr-1">SIGN IN</span>
            </v-btn>
        </v-toolbar-items>
        <v-btn icon @click='login' class="hidden-md-and-up">
            <v-icon>fa-sign-in-alt</v-icon>
        </v-btn>
    </v-toolbar>
</div>
</template>

<script>
import { mapGetters } from "vuex";
import Login from "@/components/signin/login.vue";
import { verifyToken, refreshToken } from "@/graphql/signin/token.js";
export default {
  data: function() {
    return {
      drawer: true,
      signin: false,
      logging: true
    };
  },
  components: {
    Login
  },
  mounted() {
    this.userAuthed = false;
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
  computed: {
    authed: function() {
      return this.$store.state["user"].authed;
    },
    gravataremail: function() {
      return this.$store.state["user"].gravataremail;
    }
  },
  methods: {
    login: function() {
      this.$router.push({
        name: "Login",
        query: { redirect: this.$route.path }
      });
    },
    signup: function() {},
    signout: function() {
      this.$router.push({
        name: "Signout",
        query: { redirect: this.$route.path }
      });
    }
  }
};
</script>
