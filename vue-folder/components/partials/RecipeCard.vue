<template>
  <a v-bind:href="'/apothecary/recipe/' + recipe.id" class="text-dark">
    <div class="card">
      <div class="card-body">
        <div class="card-title">ID: {{ recipe.id }}</div>
        <div class="card-subtitle mb-2 text-muted">{{ recipe.date }}</div>
        <div class="card-text">Пациент: {{ recipe.patientName }}</div>
        <div class="card-text">Доктор: {{ recipe.doctorName }}</div>
      </div>
    </div>
  </a>
</template>

<script>
  export default {
    name: "RecipeCard",
    props: {
      recipe: {
        type: Object,
        required: true
      }
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
