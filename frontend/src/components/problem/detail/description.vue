<template>
  <div class="ma-4">
    <h2
      v-if="content"
      class="headline mb-3">Content</h2>
    <div class="mb-3">{{ content }}</div>
    <h2
      v-if="standardInput"
      class="headline mb-3">Standard Input</h2>
    <div class="mb-3">{{ standardInput }}</div>
    <h2
      v-if="standardOutput"
      class="headline mb-3">Standard Output</h2>
    <div class="mb-3">{{ standardOutput }}</div>
    <h2
      v-if="constraints"
      class="headline mb-3">Constraints</h2>
    <div class="mb-3">{{ constraints }}</div>
    <h2
      v-if="resource"
      class="headline mb-3">Resource</h2>
    <div class="mb-3">{{ resource }}</div>
    <h2
      v-if="note"
      class="headline mb-3">Note</h2>
    <div class="mb-3">{{ note }}</div>
  </div>
</template>

<script>
export default {
  props: {
    content: {
      type: String,
      required: false,
      default: ''
    },
    standardInput: {
      type: String,
      required: false,
      default: ''
    },
    standardOutput: {
      type: String,
      required: false,
      default: ''
    },
    constraints: {
      type: String,
      required: false,
      default: ''
    },
    resource: {
      type: String,
      required: false,
      default: ''
    },
    note: {
      type: String,
      required: false,
      default: ''
    }
  },
  data: function () {
    return {
    }
  }
}
</script>
