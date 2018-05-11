<template>
  <input type="hidden" name="csrfmiddlewaretoken" v-bind:value="csrfToken">
</template>

<script>
  export default {
    name: "CsrfInput",
    beforeMount() {
      this.csrfToken = this.$cookies.get("csrftoken")
    },
    data() {
      return {
        csrfToken: ""
      }
    }
  }
</script>

<style lang="less" scoped>

</style>
