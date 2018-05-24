<template>
  <main role="main" class="container">
    <div class="my-3 p-3 bg-white rounded">
      <h2 class="text-center mt-2">Рецепт</h2>
      <div class="border-top p-3">
        <h4 class="text-center">ID: {{ data.id }}</h4>
        <h6 class="text-center">Кому: {{ data.patient_initials }}</h6>
        <h6 class="text-center">Кем: {{ data.doctor_initials }}</h6>
      </div>
      <table class="table mt-3 text-center">
        <thead class="thead-light">
          <tr>
            <th>Название</th>
            <th>Количество</th>
            <th>Доза</th>
            <th>Частота</th>
            <th>Длительность</th>
            <th>Выдан</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="medicine in data.requests">
            <td>{{ medicine.medicine_name }}</td>
            <td>{{ medicine.medicine_count }}</td>
            <td>{{ medicine.dosage }}</td>
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
  </main>
</template>

<script>
  import axios from 'axios';

  import Checkmark from "./partials/Checkmark";
  import Close from "./partials/Close";

  export default {
    name: "PatientRecipe",
    components: {
      Close,
      Checkmark
    },
    data() {
      return {
        data: null
      }
    },
    beforeMount() {
      console.log(this.$route.params.id);
      axios.get("/api/recipes/" + this.$route.params.id)
        .then(response => this.data = response.data);
    }
  }
</script>

<style lang="less">
</style>
