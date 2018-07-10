<template>
    <v-navigation-drawer :clipped = "$vuetify.breakpoint.lgAndUp" fixed app width = 200>
      <v-list>

        <v-list-tile>
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
</template>

<script>
    export default {

    }
</script>
