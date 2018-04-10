<template>
  <div class="form">
    <p>Войти</p>
    <form action="/login" method="post">
      <input type="hidden" name="csrfmiddlewaretoken" v-bind:value="csrfToken">
      <app-input id="email" label="E-mail" type="text"/>
      <app-input id="password" label="Пароль" type="password"/>
      <app-button name="Войти"/>
    </form>
  </div>
</template>

<script>
  import AppButton from "../partials/AppButton";
  import AppInput from "../partials/AppInput";

  export default {
    name: "LoginForm",
    components: {
      AppButton,
      AppInput
    },
    data() {
      return {
        csrfToken: ""
      }
    },
    beforeMount() {
      this.csrfToken = this.$cookies.get("csrftoken")
    }
  }
</script>

<style lang="less" scoped>
  .form {
    margin: 150px auto;
    text-align: center;
    border: 2px solid #087e8b;
    border-radius: 10px;
    width: 300px;
    height: 260px;
    background-color: #ffffff;

    p {
      font-size: 24px;
      margin-top: 20px;
      margin-bottom: 20px;
    }
  }
</style>
