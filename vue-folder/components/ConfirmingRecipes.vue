<template>
  <div>
    <apothecory-header/>
    <div class="card col-md-10 align-self-center">
      <div class="card-body">
        <div class="card-title">Рецепт Токен</div>
        <div class="card-subtitle mb-2 text-muted">Дата</div>
        <div class="card-text">ФИО пациента: ФИО</div>
        <div class="card-text">E-mail пациента</div>
        <div class="card-text">Номер полиса</div>
        <div class="card-text">Номер мед карты</div>
        <div class="card-text">Возраст</div>
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
  import ApothecoryHeader from "./header/ApothecaryHeader";
  import AppButton from "./partials/AppButton";
  import Checkmark from "./partials/Checkmark";

  export default {
    name: "ConfirmingRecipes",
    components: {
      ApothecoryHeader,
      AppButton,
      Checkmark
    },
    data() {

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
