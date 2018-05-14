<template>
  <div>
    <doctor-header/>
    <div class="card col-md-10 align-self-center">
      <div class="card-body">
        <div class="card-title">Рецепт ID: {{$route.params.id}}</div>
        <div class="card-subtitle mb-2 text-muted">{{data.date}}</div>
        <div class="card-text">ФИО пациента: {{data.patient_initials}}</div>
        <div class="card-text">E-mail пациента: {{data.patient_email}}</div>
        <div class="card-text">Номер полиса: {{data.medicine_policy_number}}</div>
        <div class="card-text">Номер мед карты: {{data.medicine_card_number}}</div>
        <div class="card-text">Возраст: {{data.patient_age}}</div>
        <div class="card-text">Действителен <checkmark/></div>
        <div class="card-text">
          <table class="table">
            <thead>
              <tr>
                <th>Лекарство</th>
                <th>Доза</th>
                <th>Частота</th>
                <th>Длительность</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(request, index) in data.requests">
                <td>{{request.medicine_name}}</td>
                <td>{{request.dosage}}</td>
                <td>{{request.medicine_frequency}}</td>
                <td>{{request.medicine_period}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import ApothecaryHeader from "./header/ApothecaryHeader";
  import AppButton from "./partials/AppButton";
  import Checkmark from "./partials/Checkmark";
  import Close from "./partials/Close";
  import Vue from "vue";

  import axios from "axios";
  import DoctorHeader from "./header/DoctorHeader";

  export default {
    name: "ConfirmingRecipes",
    components: {
      DoctorHeader,
      ApothecaryHeader,
      AppButton,
      Checkmark,
      Close
    },
    data() {
      return {
        data: {
          patient_email: "email@example.com",
          patient_initials: "Surname Name",
          medicine_policy_number: "123456",
          date: "2018-04-08 07:03",
          day_duration: 15,
          id: 1,
          medicine_card_number: "123456",
          patient_age: 18,
          doctor_email: "airatb@yandex.ru",
          requests:
          [
            {
              id: 1,
              is_accepted: false,
              medicine_period: "10 дней",
              dosage: "1 таблетка",
              medicine_name: "Парацетамол",
              medicine_frequency: "3 раза в день",
              medicine_name_id: 1,
              medicines: []
            }
          ],
          doctor_initials: "Baiburov Airat"
        },
        checked_medicines: [],
        selected_medicines: [],
        error: false,
      }
    },
    methods: {
      getRecipe() {
        axios.get("/api/recipes/" + this.$route.params.id)
         .then(function(response) {
           this.data = response.data.data;
           console.log(this.data);
         }.bind(this))
         .catch(error => {
           this.data = [];
           console.log(error);
         })
      }
    },
    beforeMount() {
      this.getRecipe();
    }
  }
</script>

<style lang="less" scoped>
  .card {
    margin: 20px auto;
    text-align: center;
    padding: 0;

    .card-title {
      font-size: 23px;
    }

    .card-text {
      margin-top: 10px;
    }

    .card-footer {
      padding: 0;
    }
  }
</style>
