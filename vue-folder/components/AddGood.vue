<template>
  <div>
    <apothecary-header/>
    <div class="create-medicine-form">
      <h4>Добавить лекарство</h4>

      <hr>

      <div class="form-group">
        <label for="newMedicineNameInput">Название препарата</label>
        <input type="text" class="form-control" id="newMedicineNameInput" v-model="newMedicine.name">
      </div>

      <div class="form-group">
        <label for="newMedicineTypeInput">Тип препарата</label>
        <input type="text" class="form-control" id="newMedicineTypeInput" v-model="newMedicine.type">
      </div>

      <div class="form-group">
        <label for="description">Описание</label>
        <input type="text" v-model="newMedicine.description" class="form-control" id="description" name="description"/>
      </div>

      <div class="form-group">
        <label for="newMedicineLevelInput">Уровень содержания наркотиков</label>
        <select class="form-control" id="newMedicineLevelInput" v-model="newMedicine.level">
          <option>0</option>
          <option>1</option>
          <option>2</option>
        </select>
      </div>

      <div class="form-group">
        <label for="newMedicineCountInput">Количество</label>
        <input type="number" class="form-control" id="newMedicineCountInput" v-model="newMedicine.count">
      </div>

      <div class="form-group">
        <label for="newMedicinePriceInput">Цена</label>
        <input type="number" class="form-control" id="newMedicinePriceInput" v-model="newMedicine.price">
      </div>

      <button class="btn btn-primary" v-on:click="addMedicine">Добавить лекарство</button>
      <button class="btn btn-danger" v-on:click="back">Назад</button>
    </div>
  </div>
</template>

<script>
  import axios from "axios";

  import AddGoodForm from "./forms/AddGoodForm";
  import ApothecaryHeader from "./header/ApothecaryHeader";

  export default {
    name: "AddGood",
    components: {
      AddGoodForm,
      ApothecaryHeader
    },
    data() {
      return {
        newMedicine: {
          name: "",
          type: "",
          description: "",
          level: 0,
          count: 0,
          price: 0
        }
      }
    },
    methods: {
      addMedicine() {
        axios.post("/api/medicines/new", this.newMedicine, {
          headers: {
            "X-CSRFTOKEN": this.$cookies.get("csrftoken")
          }
        }).then(response => window.location = '/apothecary/' + response.data.data.id);
      },
      back() {
        window.location = "/apothecary";
      }
    }
  }
</script>

<style lang="less" scoped>
  .create-medicine-form {
    border: 2px solid #087e8b;
    width: 450px;
    height: auto;
    margin: 20px auto;
    border-radius: 10px;
    background-color: #fff;
    text-align: center;
    padding: 20px;

    hr {
      color: #087e8b;
      background-color: #087e8b;
      border: none;
      height: 1px;
    }

    button {
      margin-top: 20px;
    }
  }
</style>
