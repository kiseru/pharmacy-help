<template>
  <div>
    <apothecory-header/>
    <div class="card col-md-10 align-self-center">
      <div class="card-body">
        <div class="card-title">Рецепт {{ data.id }}</div>
        <div class="card-subtitle mb-2 text-muted">{{ data.date }}</div>
        <div class="card-text">ФИО пациента: {{ data.patient_initials }}</div>
        <div class="card-text">E-mail: {{ data.patient_email }}</div>
        <div class="card-text">Номер полиса: {{ data.medicine_policy_number }}</div>
        <div class="card-text">Номер мед карты: {{ data.medicine_card_number }}</div>
        <div class="card-text">Возраст: {{ data.patient_age }}</div>
        <div class="card-text">
          <table class="table">
            <thead class="thead-light">
              <tr>
                <th>Название</th>
                <th>Тип</th>
                <th>Количество</th>
                <th>Доза</th>
                <th>Частота</th>
                <th>Длительность</th>
                <th>Выдан</th>
                <th>Выдать</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="medicine in data.requests">
                <td>{{ medicine.medicine_name }}</td>
                <td>
                  <select class="custom-select custom-select-sm" v-model="medicine.given_medicine">
                    <option selected>Выберите тип</option>
                    <option v-bind:value="good.id" v-for="good in medicine.goods" v-if="good.count > medicine.medicine_count">{{ good.type }}</option>
                  </select>
                </td>
                <td>{{ medicine.medicine_count }}</td>
                <td>{{ medicine.dosage }}</td>
                <td>{{ medicine.medicine_frequency }}</td>
                <td>{{ medicine.medicine_period }}</td>
                <td>
                  <checkmark v-if="medicine.is_accepted"/>
                  <close v-else />
                </td>
                <td><input type="checkbox" class="form-check-input" v-bind:disabled="medicine.is_accepted" v-model="medicine.accept"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="card-footer">
        <button class="btn btn-primary m-2" v-on:click="confirm">Выдать</button>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  import ApothecoryHeader from "./header/ApothecaryHeader";
  import AppButton from "./partials/AppButton";
  import Checkmark from "./partials/Checkmark";
  import Close from "./partials/Close";

  export default {
    name: "ConfirmingRecipes",
    components: {
      ApothecoryHeader,
      AppButton,
      Checkmark,
      Close
    },
    data() {
      return {
        data: null
      }
    },
    beforeMount() {
      axios.get(`/api/recipes/${this.$route.params.id}/confirm`)
        .then(response => {
          this.data = response.data;
          this.data.requests.forEach(medicine => medicine.accept = false);
        });
    },
    methods: {
      confirm() {
        let requests = this.data.requests.filter(medicine => medicine.accept)
          .map(medicine => {
            let request = {};
            request.id = medicine.id;
            request.given_medicine = medicine.given_medicine;
            request.medicine_count = medicine.medicine_count;
            return request;
          });
        axios.post(`/api/recipes/${this.$route.params.id}`, { requests: requests }, {
        	headers: { "X-CSRFTOKEN": this.$cookies.get("csrftoken") }
        }).then(response => window.location = "/apothecary/recipes");
      }
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
