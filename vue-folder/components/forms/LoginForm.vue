<template>
  <div class="card">
    <div class="card-title">Войти</div>

    <div class="form-group">
      <label for="userEmailInput">E-mail</label>
      <input type="text" class="form-control" id="userEmailInput" v-model="user.email" v-on:keyup.enter="login">
      <div class="validate-error" v-if="!isEmailValid">Неправильно введен E-mail</div>
    </div>

    <div class="form-group">
      <label for="userPasswordInput">Пароль</label>
      <input type="password" class="form-control" id="userPasswordInput" v-model="user.password" v-on:keyup.enter="login">
      <div class="validate-error" v-if="!isPasswordValid">Пароль может содержать только A-Za-z0-9</div>
    </div>

    <div class="validate-error" v-if="error">Неправильный E-mail или пароль</div>

    <button class="btn btn-primary" v-on:click="login">Войти</button>
  </div>
</template>

<script>
  import axios from "axios";

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
        user: {
          email: "",
          password: ""
        },
        isEmailValid: true,
        isPasswordValid: true,
        error: false
      }
    },
    methods: {
      login: function() {
        const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        this.isEmailValid = this.user.email.search(emailRegex) !== -1;

        const passwordRegex = /^[A-Za-z0-9]{8,}$/;
        this.isPasswordValid = this.user.password.search(passwordRegex) !== -1;

        if (!this.isPasswordValid && !this.isEmailValid) return;

        axios.post("/api/login", this.user, {
        	headers: { "X-CSRFTOKEN": this.$cookies.get("csrftoken") }
        }).then(response => {
        	this.error = false;
        	window.location = response.data.location;
        }, error => this.error = true);
      }
    }
  }
</script>

<style lang="less" scoped>
  .card {
    margin: 0 auto;
    width: 400px;
    padding: 20px;

    .card-title {
      font-size: 23px;
      text-align: center;
    }

    .validate-error {
      color: #dc3545;
      font-size: 12px;
    }

    button {
      width: 100px;
      margin: 10px auto 0 auto;
    }
  }
</style>
