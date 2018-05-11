<template>
  <div class="my-form">
    <p>{{ header }}</p>
    <form v-bind:action="action" method="post">
      <csrf-input/>
      <app-input v-for="input in inputs" v-bind:id="input.id" v-bind:label="input.label" v-bind:type="input.type"/>
      <app-button v-bind:name="buttonName"/>
    </form>
  </div>
</template>

<script>
  import AppButton from "../partials/AppButton";
  import AppInput from "../partials/AppInput";
  import CsrfInput from "./CsrfInput";

  export default {
    name: "AppForm",
    components: {
      AppButton,
      AppInput,
      CsrfInput
    },
    data() {
      return {
        csrfToken: ""
      }
    },
    props: {
      header: {
        required: true
      },
      buttonName: {
        required: true
      },
      action: {
        required: true
      },
      inputs: {
        type: Array,
        required: true
      }
    },
    mount(){
      console.log(this);
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
