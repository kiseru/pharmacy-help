<template>
  <div>
    <apothecary-header v-if="user.role == 'apothecary'"/>
    <doctor-header v-else/>

    <div class="create-new-worker-form">
      <h4>Добавить сотрудника</h4>

      <hr>

      <div class="form-group">
        <label for="newWorkerFirstNameInput">Имя</label>
        <input type="text" class="form-control" id="newWorkerFirstNameInput" v-model="newWorker.first_name">
      </div>

      <div>
        <label for="newWorkerLastNameInput">Фамилия</label>
        <input type="text" class="form-control" id="newWorkerLastNameInput" v-model="newWorker.last_name">
      </div>

      <div>
        <label for="newWorkerEmailInput">E-mail</label>
        <input type="text" class="form-control" id="newWorkerEmailInput" v-model="newWorker.email">
        <div class="validate-error" v-if="!isEmailValid">Неправильно введен E-mail</div>
      </div>

      <div>
        <label for="newWorkerPhoneNumberInput">Номер телефона</label>
        <input type="text" class="form-control" id="newWorkerPhoneNumberInput" v-model="newWorker.phone_number">
        <div class="validate-error" v-if="!isPhoneValid">Номер телефона должен иметь формат +7*********</div>
      </div>

      <div>
        <label for="newWorkerPasswordInput">Пароль</label>
        <input type="password" class="form-control" id="newWorkerPasswordInput" v-model="newWorker.password">
        <div class="validate-error" v-if="!isPasswordValid">Пароль может содержать только A-Za-z0-9</div>
      </div>

      <div>
        <label for="newWorkerMatchPasswordInput">Повторите пароль</label>
        <input type="password" class="form-control" id="newWorkerMatchPasswordInput" v-model="newWorker.matchPassword">
        <div class="validate-error" v-if="!arePasswordsSame">Пароли не совпадают</div>
      </div>
      <div class="validate-error" v-if="error">Ошибка</div>
      <hr>

      <button type="button" class="btn btn-success" v-on:click="addWorker">Добавить сотрудника</button>
    </div>
  </div>
</template>

<script>
  import AppButton from "./partials/AppButton";
  import DefaultHeader from "./header/DefaultHeader";

  import axios from "axios";

  export default {
    name: "CreatingWorker",
    components: {
      AppButton,
      DefaultHeader
    },
    data() {
      return {
        newWorker: {
          first_name: "",
          last_name: "",
          email: "",
          phone_number: "",
          password: "",
          matchPassword: ""
        },
        isEmailValid: true,
        isPasswordValid: true,
        arePasswordsSame: true,
        isPhoneValid: true,
        error: false,
      }
    },
    computed: {
      user(){
        return this.$store.getters.getUser;
      }
    },
    methods: {
      addWorker() {
        const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        this.isEmailValid = this.newWorker.email.search(emailRegex) !== -1;

        const passwordRegex = /^[A-Za-z0-9]{8,}$/;
        this.isPasswordValid = this.newWorker.password.search(passwordRegex) !== -1;

        this.arePasswordsSame = this.newWorker.password == this.newWorker.matchPassword;

        const phoneRegex = /^\+7\d{9}$/;
        this.isPhoneValid = this.newWorker.phone_number.search(phoneRegex) !== -1;

        if (!this.isPasswordValid ||
            !this.isEmailValid ||
            !this.arePasswordsSame ||
            !this.isPhoneValid
        ) return;

        axios.post("/api/workers/new", this.newWorker, {
        	headers: { "X-CSRFTOKEN": this.$cookies.get("csrftoken") }
        }).then(response => {
        	this.error = false;
        	window.location = '/' + this.user().role + '/workers/' + response.data.data.id ;
        }, error => this.error = true);
      }
    }
  }
</script>

<style lang="less" scoped>
  .create-new-worker-form {
    border: 2px solid #007bff;
    width: 550px;
    height: auto;
    margin: 20px auto;
    border-radius: 10px;
    background-color: #fff;
    text-align: center;
    padding: 20px;

    hr {
      color: #007bff;
      background-color: #007bff;
      border: none;
      height: 1px;
    }

    button {
      margin-top: 20px;
    }
    .validate-error {
      color: #dc3545;
      font-size: 12px;
    }
  }
</style>
