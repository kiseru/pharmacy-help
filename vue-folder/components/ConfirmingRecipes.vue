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
              <tr>
                <td>Название</td>
                <td>
                  <select class="custom-select custom-select-sm">
                    <option selected>Выберити тип</option>
                    <option value="1">Таблетки</option>
                    <option value="2">Спрей</option>
                  </select>
                </td>
                <td>3</td>
                <td>1</td>
                <td>100г</td>
                <td>2 раза в день</td>
                <td>3 недели</td>
                <td><checkmark/></td>
                <td><input type="checkbox" class="form-check-input" disabled></td>
              </tr>
              <tr>
                <td>Название</td>
                <td>
                  <select class="custom-select custom-select-sm">
                    <option selected>Выберити тип</option>
                    <option value="1">Таблетки</option>
                    <option value="2">Спрей</option>
                  </select>
                </td>
                <td>3</td>
                <td>1</td>
                <td>100г</td>
                <td>2 раза в день</td>
                <td>3 недели</td>
                <td><close/></td>
                <td><input type="checkbox" class="form-check-input"></td>
              </tr>
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
