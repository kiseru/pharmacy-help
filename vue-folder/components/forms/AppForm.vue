<template>
  <div class="form">
    <p>{{ header }}</p>
    <form v-bind:action="action" method="post">
      <input type="hidden" name="csrfmiddlewaretoken" v-bind:value="csrfToken">
      <app-input v-for="input in inputs" v-bind:id="input.id" v-bind:label="input.label" v-bind:type="input.type"/>
      <app-button v-bind:name="buttonName"/>
    </form>
  </div>
</template>

<script>
  import AppButton from "../partials/AppButton";
  import AppInput from "../partials/AppInput";

  export default {
    name: "AppForm",
    components: {
      AppButton,
      AppInput
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
    beforeMount() {
      this.csrfToken = this.$cookies.get("csrftoken")
    }
  }
</script>

<style scoped>
  .form {
    border: 2px solid #087E8B;
    width: 400px;
    margin: 20px auto;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
  }

  .form p {
    font-size: 22px;
    margin: 0 auto 10px;
  }

  .form input {
    margin: 5px;
  }

  .form button {
    margin-top: 10px;
    background-color: #087e8b;
    outline: none;
    border: 2px solid #087e8b;
    border-radius: 5px;
    height: 30px;
    width: 100px;
    color: #f5f5f5;
  }
</style>
