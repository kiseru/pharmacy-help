<template>
  <div>
    <apothecory-header/>
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
                <th>Название</th>
                <th>Тип</th>
                <th>Количество</th>
                <th>Уровень</th>
                <th>Доза</th>
                <th>Частота</th>
                <th>Длительность</th>
                <th>Выдан</th>
                <th>Выдать</th>
              </tr>
            </thead>
            <tbody>

            </tbody>
          </table>
        </div>
      </div>
      <div class="card-footer">
        <app-button  name="Выдать"/>
      </div>
    </div>
  </div>
</template>

<script>
  import ApothecaryHeader from "./header/ApothecaryHeader";
  import AppButton from "./partials/AppButton";
  import Checkmark from "./partials/Checkmark";

  import axios from "axios";

  export default {
    name: "ConfirmingRecipes",
    components: {
      ApothecaryHeader,
      AppButton,
      Checkmark
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
              medicine_dosage: "1 таблетка",
              medicine_name: "Парацетамол",
              medicine_frequency: "3 раза в день",
              medicine_name_id: 1
            }
          ],
          doctor_initials: "Baiburov Airat"
        }
      }
    },
    beforeMount() {
      axios.get("/api/recipes/" + this.$route.params.id)
         .then(response => this.data = response.data.data)
         .catch(error => this.data = [])
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
