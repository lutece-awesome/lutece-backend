<template>
  <v-layout
    row
    wrap>
    <v-flex
      xs12
      sm6>
      <v-select
        v-model = "language"
        :items = "items"
        width="100"/>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data: () => ({
    language: {
      text: 'GNU G++17',
      value: 'GNU G++'
    },
    items: [{
      text: 'GNU G++17',
      value: 'GNU G++'
    },
    {
      text: 'GNU GCC 7.3',
      value: 'GNU GCC'
    },
    {
      text: 'Clang 6.0.0',
      value: 'Clang'
    },
    {
      text: 'Python 3.6.5',
      value: 'Python'
    },
    {
      text: 'Java 10',
      value: 'Java'
    },
    {
      text: 'Go 1.10.2',
      value: 'Go'
    },
    {
      text: 'Ruby 2.5.1',
      value: 'Ruby'
    },
    {
      text: 'Rust 1.26.1',
      value: 'Rust'
    }]
  })
}
</script>
