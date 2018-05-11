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
              <th>Тип</th>
              <th>Количество</th>
              <th>Уровень</th>
              <th>Доза</th>
              <th>Частота</th>
              <th>Длительность</th>
              <th>Выдан</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="medicine in recipe.medicines">
              <td>{{ medicine.name }}</td>
              <td>{{ medicine.type }}</td>
              <td>{{ medicine.count }}</td>
              <td>{{ medicine.level }}</td>
              <td>{{ medicine.dosage }}</td>
              <td>{{ medicine.frequency }}</td>
              <td>{{ medicine.period }}</td>
              <td>
                <checkmark v-if="medicine.confirmed"/>
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
          date: "24.03.1995",
          token: "asdfasdfa",
          duration: 3,
          medicines: [
            {
              name: "name",
              type: "type",
              count: 45,
              level: 0,
              dosage: "dosage",
              frequency: "frequency",
              period: "period",
              confirmed: true
            },
            {
              name: "name",
              type: "type",
              count: 45,
              level: 0,
              dosage: "dosage",
              frequency: "frequency",
              period: "period",
              confirmed: false
            }
          ]
        }
      }
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
