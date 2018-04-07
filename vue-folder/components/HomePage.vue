<template>
  <div>
    <home-page-form/>
  </div>
</template>

<script>
  import HomePageForm from './forms/HomePageForm';

  export default {
    name: "HomePage",
    components: {
      HomePageForm
    },
    data() {
      return {
        isLoginForm: true
      }
    }
  }
</script>

<style lang="less" scoped>

</style>
