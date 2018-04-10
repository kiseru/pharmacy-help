<template>
  <app-form header="Добавить препорат" button-name="Добавить" action="/" v-bind:inputs="inputs"/>
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
          }
        ]
      }
    }
  }
</script>

<style lang="less" scoped>
</style>
