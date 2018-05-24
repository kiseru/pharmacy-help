<template>
  <div class="card">
    <div class="card-body">
      <div class="card-title">ID: {{ recipe.id }}</div>
      <div class="card-subtitle mb-2 text-muted">{{ recipe.date }}</div>
      <div class="card-text">Пациент: {{ recipe.patientName }}</div>
      <div class="card-text">Доктор: {{ recipe.doctorName }}</div>
    </div>
  </div>
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
  .recipe {
    border: 2px solid #087e8b;
    margin: 20px;
    height: 205px;
    background-color: #ffffff;
    border-radius: 10px;
    min-width: 500px;
    padding: 20px;
    font-size: 22px;
    text-align: right;

    .id {
      font-size: 20px;
      margin-bottom: 20px;
    }

    .recipe-date {
      margin-top: 30px;
      font-size: 18px;
      text-align: left;
    }
  }

  .card {
    margin: 10px;
  }
</style>
