<template>
  <a v-bind:href="'/apothecary/recipe/' + recipe.id" class="text-dark" v-if="isUserApothecary">
    <div class="card">
      <div class="card-body">
        <div class="card-title">ID: {{ recipe.id }}</div>
        <div class="card-subtitle mb-2 text-muted">{{ recipe.date }}</div>
        <div class="card-text">Пациент: {{ recipe.patientName }}</div>
        <div class="card-text">Доктор: {{ recipe.doctorName }}</div>
      </div>
    </div>
  </a>

  <div class="card" v-else-if="isUserDoctor">
      <div class="card-body">
        <div class="card-title">ID: {{ recipe.id }}</div>
        <div class="card-subtitle mb-2 text-muted">{{ recipe.date }}</div>
        <div class="card-text">Пациент: {{ recipe.patientName }}</div>
        <div class="card-text">Доктор: {{ recipe.doctorName }}</div>
      </div>
    </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: "RecipeCard",
    props: {
      recipe: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        isUserDoctor: false,
        isUserApothecary: false
      }
    },
    beforeMount() {
      axios.get("/api/user")
        .then(response => {
          if (response.data.role === "doctor") this.isUserDoctor = true;
          else if (response.data.role === "apothecary") this.isUserApothecary = true; 
        });
    }
  }
</script>

<style lang="less" scoped>
  a:hover {
    text-decoration: none;

    .card:hover {
      border-color: #007bff;
    }
  }
</style>
