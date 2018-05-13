<template>
  <!--<app-form header="Добавить препарат" button-name="Добавить" action="/" v-bind:inputs="inputs"/>-->
  <div class="my-form">
    <p>Добавить товар</p>
    <div>
      <csrf-input/>
      <div class="form-group">
        <label for="name">Название</label>
        <input type="text" v-model="data.name" class="form-control" id="name" name="name"/>
      </div>
      <div class="form-group">
        <label for="type">Тип</label>
        <input type="text" v-model="data.type" class="form-control" id="type" name="type"/>
      </div>
      <div class="form-group">
        <label for="description">Описание</label>
        <input type="text" v-model="data.description" class="form-control" id="description" name="description"/>
      </div>
      <div class="form-group">
        <label for="count">Количество</label>
        <input type="number" v-model="data.count" min="1" value="1" class="form-control" id="count" name="count"/>
      </div>
      <div class="form-group">
        <label for="level">Уровень (0-2)</label>
        <input type="number" v-model="data.level" min="0" value="0" max="2" class="form-control" id="level" name="level"/>
      </div>
      <div class="form-group">
        <label for="price">Цена</label>
        <input type="number" step="0.01" min="0.00" v-model="data.price" class="form-control" id="price" name="price" />
      </div>
      <!--<app-button v-bind:name="buttonName"/>-->
      <button type="submit" class="btn btn-primary" v-on:click="addGood">Добавить</button>
    </div>
  </div>
</template>

<script>
  import AppButton from "../partials/AppButton";
  import AppInput from "../partials/AppInput";
  import AppForm from "./AppForm";
  import axios from "axios";

  export default {
    name: "AddGoodForm",
    components: {
      AppButton,
      AppInput,
      AppForm
    },
    data() {
      return {
        inputs: [
          {
            id: "name",
            label: "Название",
          },
          {
            id: "description",
            label: "Описание"
          },
          {
            id: "count",
            label: "Количетсво"
          },
          {
            id: "level",
            label: "Уровень (1-3)"
          },
          {
            id: "price",
            label: "Цена"
          }
        ],
        data: {
          'name': '',
          'type': '',
          'description': '',
          'count': '1',
          'price': '0.00',
          'level': 0,
        }
      }
    },
    methods: {
      addGood() {
        console.log('add good');
        console.log(this.data);
        axios.post("/api/test/medicines/new", this.data, {
        	headers: { "X-CSRFTOKEN": this.$cookies.get("csrftoken") }
        }).then(response => {
        	this.error = false;
        	window.location = '/apothecary'
        }, error => this.error = true);
      }
    }
  }
</script>

<style lang="less" scoped>
  .my-form {
    border: 2px solid #2e6da4;
    width: 400px;
    margin: 20px auto;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    background-color: #fff;

    p {
      font-size: 22px;
      margin: 0 auto 10px;
    }
  }
</style>
