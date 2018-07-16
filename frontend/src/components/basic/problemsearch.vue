<template>
  <!-- <v-autocomplete
        v-model = "model"
        :items = "items"
        :loading = "isLoading"
        :search-input.sync = "search"
        hide-no-data
        hide-selected

        append-icon = ''
        prepend-icon="mdi-magnify"
        return-object
    >
        <v-slide-transition
          slot="append-inner"
        >
            <v-list>
                <v-list-tile v-for = "( each , index ) in items" :key = "index" >
                    <v-list-tile-title>
                        {{ each.title }}
                    </v-list-tile-title>
                </v-list-tile>
            </v-list>
        </v-slide-transition> -->
  <v-autocomplete
    v-model = "model"
    :items = "items"
    :loading = "isLoading"
    :search-input.sync = "search"
    single-line
    hide-details
    hide-no-data
    append-icon="mdi-magnify"
    return-object
    small-chips
    label="Search"/>
</template>

<script>
import { ProblemSearchGQL } from '@/graphql/problem/search.js'
export default {
  data: function () {
    return {
      model: null,
      result: [],
      isLoading: false,
      search: null
    }
  },

  computed: {
    items () {
      return this.result
    }
  },

  watch: {
    search (val) {
      if (!val || val.length === 0 || this.isLoading) return
      this.isLoading = true
      this.$apollo.query({
        query: ProblemSearchGQL,
        variables: {
          title: val
        }
      })
        .then(response => response.data.problemsearch)
        .then(data => {
          this.result = data
        })
        .finally(() => (this.isLoading = false))
    }
  }
}
</script>
