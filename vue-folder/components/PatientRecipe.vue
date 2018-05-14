<template>
  <div>
    <default-header/>
    <div class="card">
      <div class="card-title">Рецепт</div>
      <div class="card-body">
        <table class="table">
          <thead>
            <tr>
              <th>Название</th>
              <th>Доза</th>
              <th>Частота</th>
              <th>Длительность</th>
              <th>Выдан</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="medicine in recipe.requests">
              <td>{{ medicine.medicine_name }}</td>
              <td>{{ medicine.medicine_dosage }}</td>
              <td>{{ medicine.medicine_frequency }}</td>
              <td>{{ medicine.medicine_period }}</td>
              <td>
                <checkmark v-if="medicine.is_accepted"/>
                <close v-else/>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  import DefaultHeader from "./header/DefaultHeader";
  import Checkmark from "./partials/Checkmark";
  import Close from "./partials/Close";
  import axios from 'axios';

  export default {
    name: "PatientRecipe",
    components: {
      Close,
      Checkmark,
      DefaultHeader
    },
    data() {
      return {
        recipe: {
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
            }
          ],
          doctor_initials: "Baiburov Airat"
        }
      }
    },
    methods: {
      getRecipe() {
        axios.get("/api/recipes/" + this.$route.params.id)
         .then(function(response) {
           this.recipe = response.data.data;
           console.log(this.data);
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
    width: 1000px;
    margin: 20px auto;

    .card-title {
      font-size: 32px;
      text-align: center;
    }
  }
</style>
