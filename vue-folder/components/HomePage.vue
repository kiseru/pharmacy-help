<template>
  <div>
    <login-form/>
  </div>
</template>

<script>
  import LoginForm from './forms/LoginForm';

  export default {
    name: "HomePage",
    components: {
      LoginForm
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
