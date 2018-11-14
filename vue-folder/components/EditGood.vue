<template>
  <div>
    <default-header/>
    <main role="main" class="continer mt-4">
      <div class="d-block mx-auto p-4 bg-white text-center w-50">
        <h3>Информация о товаре</h3>

        <h6>Название: {{ medicine.name }}</h6>
        <h6>Тип: {{ medicine.type }}</h6>
        
        <div class="form-group w-50 mx-auto">
          <label for="countInput">Количество</label>
          <div class="input-group">
            <input type="text" class="form-control text-right" id="countInput" v-model="medicine.count">
            <div class="input-group-prepend">
              <div class="input-group-text px-2">шт</div>
            </div>
          </div>
        </div>

        <div class="form-group w-50 mx-auto">
          <label for="priceInput">Цена</label>
          <div class="input-group">
            <input type="text" class="form-control text-right" id="priceInput" v-model="medicine.price">
            <div class="input-group-prepend">
              <div class="input-group-text">&#x20bd;</div>
            </div>
          </div>
        </div>

        <button class="btn btn-primary mt-2" v-on:click="change">Изменить</button>
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";

import DefaultHeader from "./header/DefaultHeader";

export default {
  name: "EditRecipe",
  components: {
    DefaultHeader
  },
  data() {
    return {
      medicine: null
    }
  },
  beforeMount() {
    axios.get(`/api/medicines/${this.$route.params.id}`)
      .then(response => this.medicine = response.data);
  },
  methods: {
    change() {
      axios.post(`/api/medicines/${this.medicine.id}`, { count: this.medicine.count, price: this.medicine.price }, {
        headers: { "X-CSRFTOKEN": this.$cookies.get("csrftoken") }
      }).then(response => window.location = "/apothecary");
    }
  }
}
</script>

<style lang="less">

</style>
