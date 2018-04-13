<template>
  <app-form header="Добавить препарат" button-name="Добавить" action="/" v-bind:inputs="inputs"/>
</template>

<script>
  import AppButton from "../partials/AppButton";
  import AppInput from "../partials/AppInput";
  import AppForm from "./AppForm";

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
        ]
      }
    }
  }
</script>

<style lang="less" scoped>
</style>
