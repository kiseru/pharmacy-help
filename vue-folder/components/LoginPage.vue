<template>
  <div class="form-signin">
    <h1 class="h3 mb-3 font-weight-norma">Вход</h1>

    <label for="inputEmail" class="sr-only">E-mail</label>
    <input type="email" id="inputEmail" class="form-control" placeholder="E-mail" autofocus v-model="user.email">

    <label for="inputPassword" class="sr-only">Password</label>
    <input type="password" id="inputPassword" class="form-control" placeholder="Пароль" v-model="user.password">

    <div class="mb-2 text-danger" v-if="!isEmailValid || !isPasswordValid || error">Неправильно введен E-mail или пароль</div>

    <button class="btn btn-lg btn-primary btn-block" v-on:click="login">Войти</button>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: "HomePage",
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
  .form-signin {
    width: 100%;
    max-width: 330px;
    padding: 15px;
    margin: auto;

    input[type="email"] {
      margin-bottom: -1px;
      border-bottom-right-radius: 0;
      border-bottom-left-radius: 0;
    }

    input[type="password"] {
      margin-bottom: 10px;
      border-top-left-radius: 0;
      border-top-right-radius: 0;
    }

    .validate-error {
      color: #dc3545;
      font-size: 12px;
    }
  }
</style>
