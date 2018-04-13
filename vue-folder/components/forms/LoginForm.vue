<template>
  <app-form header="Войти" button-name="Войти" action="/login" v-bind:inputs="inputs"/>
</template>

<script>
  import AppButton from "../partials/AppButton";
  import AppInput from "../partials/AppInput";
  import AppForm from "./AppForm";

  export default {
    name: "LoginForm",
    components: {
      AppButton,
      AppForm,
      AppInput
    },
    data() {
      return {
        inputs: [
          {
            id: "email",
            label: "E-mail"
          },
          {
            id: "password",
            label: "Пароль",
            type: "password"
          }
        ]
      }
    }
  }
</script>

<style lang="less" scoped>
  .form {
    margin-top: 200px !important;
  }
</style>
