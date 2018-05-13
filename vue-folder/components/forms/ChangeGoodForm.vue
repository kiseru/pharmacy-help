<template>
  <!--<app-form header="Добавить препарат" button-name="Добавить" action="/" v-bind:inputs="inputs"/>-->
  <div class="my-form">
    <p>Редактировать информацию о товаре</p>
    <div>
      <div class="form-group">
        <div class="card-text">Название: {{good.name}}</div>
      </div>
      <div class="form-group">
        <div class="card-text">Тип: {{good.type}}</div>
      </div>
      <div class="form-group">
        <div class="card-text">Описание: {{good.description}}</div>
      </div>

      <div class="form-group">
        <div class="card-text">Уровень (0-2): {{good.level}}</div>
      </div>
      <div class="form-group">
        <label for="count">Количество</label>
        <input type="number" v-model="good.count" min="1" value="1" class="form-control" id="count" name="count"/>
      </div>
      <div class="form-group">
        <label for="price">Цена</label>
        <input type="number" step="0.01" min="0.00" v-model="good.price" class="form-control" id="price" name="price" />
      </div>
      <!--<app-button v-bind:name="buttonName"/>-->
      <button type="submit" class="btn btn-primary" v-on:click="updateGood">Сохранить</button>
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
        good: {
          'name': '',
          'type': '',
          'description': '',
          'count': '0',
          'price': '0.00',
          'level': 0,
        }
      }
    },
    methods: {
      updateGood() {
        console.log('add good');
        console.log(this.good);
        axios.post("/api/test/medicines/" + this.$route.params.id, this.good, {
        	headers: { "X-CSRFTOKEN": this.$cookies.get("csrftoken") }
        }).then(response => {
        	this.error = false;
        	window.location = '/apothecary'
        }, error => this.error = true);
      },
      getGood() {
        axios.get("/api/test/medicines/" + this.$route.params.id)
         .then(function(response) {
           this.good = response.data;
           console.log(this.good);
         }.bind(this))
         .catch(error => {
           console.log(error)
         })
      }
    },
    beforeMount() {
      this.getGood();
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
