<template>
  <div>
    <default-header/>
    
    <div class="create-new-worker-form">
      <h4>Добавить сотрудника</h4>

      <hr>

      <div class="form-group">
        <label for="newWorkerFirstNameInput">Имя</label>
        <input type="text" class="form-control" id="newWorkerFirstNameInput" v-model="newWorker.firstName">
      </div>

      <div>
        <label for="newWorkerLastNameInput">Фамилия</label>
        <input type="text" class="form-control" id="newWorkerLastNameInput" v-model="newWorker.lastName">
      </div>

      <div>
        <label for="newWorkerEmailInput">E-mail</label>
        <input type="text" class="form-control" id="newWorkerEmailInput" v-model="newWorker.email">
      </div>

      <div>
        <label for="newWorkerPhoneNumberInput">Номер телефона</label>
        <input type="text" class="form-control" id="newWorkerPhoneNumberInput" v-model="newWorker.phoneNumber">
      </div>

      <div>
        <label for="newWorkerPasswordInput">Пароль</label>
        <input type="password" class="form-control" id="newWorkerPasswordInput" v-model="newWorker.password">
      </div>

      <div>
        <label for="newWorkerMatchPasswordInput">Повторите пароль</label>
        <input type="password" class="form-control" id="newWorkerMatchPasswordInput" v-model="newWorker.matchPassword">
      </div>

      <hr>

      <button type="button" class="btn btn-success" v-on:click="add()">Добавить сотрудника</button>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  import AppButton from "./partials/AppButton";
  import DefaultHeader from "./headers/DefaultHeader";

  export default {
    name: "CreatingWorker",
    components: {
      AppButton,
      DefaultHeader
    },
    data() {
      return {
        newWorker: {
          firstName: "",
          lastName: "",
          email: "",
          phoneNumber: "",
          password: "",
          matchPassword: ""
        }
      }
    },
    methods: {
      add() {
        axios.post({
          email: this.newWorker.email,
          phone_number: this.newWorker.phoneNumber,
          last_name: this.newWorker.lastName,
          first_name: this.newWorker.firstName,
          password: this.newWorker.password
        })
        windows.location = "/workers"
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
  }
</style>
