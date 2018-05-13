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
                <th>Доза</th>
                <th>Частота</th>
                <th>Длительность</th>
                <th>Выдан</th>
                <th>Выдать</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(request, index) in data.requests">
                <td>{{request.medicine_name}}</td>
                <td>
                  <select class="custom-select custom-select-sm" v-model="selected_medicines[index]">
                    <option v-for="option in request.medicines" v-bind:value="option.id">
                      {{ option.name }} {{option.type}}
                    </option>
                  </select>
                </td>
                <td>{{request.medicine_dosage}}</td>
                <td>{{request.medicine_frequency}}</td>
                <td>{{request.medicine_period}}</td>
                <td v-if="request.is_accepted"><checkmark/></td>
                <td v-else><close/></td>
                <td v-if="request.is_accepted"><input type="checkbox" class="form-check-input"  disabled></td>
                <td v-else><input type="checkbox" class="form-check-input" v-bind:value="request.medicine_name_id" v-model="checked_medicines[index]"></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="card-footer">
        <button class="btn btn-primary" v-on:click="confirmRecipe"> Выдать</button>
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

  export default {
    name: "ConfirmingRecipes",
    components: {
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
              medicine_dosage: "1 таблетка",
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
      confirmRecipe: function() {
        console.log('clicked');
        console.log(this.checked_medicines);
        console.log(this.selected_medicines);
        let result = [];
        this.checked_medicines.forEach((v, k)=> {
          if (v) {
            result.push({
              'medicine_id': this.selected_medicines[k],
              'medicine_name_id': this.data.requests[k].medicine_name_id,
              'medicine_count': 1
            })
          }
        });
        console.log(result);
        axios.post('/api/recipes/' + this.$route.params.id, result, {
        	headers: { "X-CSRFTOKEN": this.$cookies.get("csrftoken") }
        })
          .then(
            response => {
        	    this.error = false;
        	    this.getRecipe();
            },
            error => this.error = true)
      },
      getRecipe() {
        axios.get("/api/recipes/" + this.$route.params.id)
         .then(function(response) {
           this.data = response.data.data;
           console.log(this.data);
           this.data.requests.forEach((v, i) => {
             Vue.set(v, 'medicines', []);
             axios.get('/api/medicines/?name_id=' + v['medicine_name_id']).then(
               response => v.medicines = response.data,
             )
           })
         }.bind(this))
         .catch(error => {
           this.data = [];
           console.log(error)
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
