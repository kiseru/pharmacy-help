<template>
  <div class="form">
    <p>Войти</p>
    <form action="/login" method="post">
      <input type="hidden" name="csrfmiddlewaretoken" v-bind:value="csrfToken">
      <div>
        <label for="email">E-mail</label>
        <br>
        <input type="text" id="email" name="email">
      </div>
      <div>
        <label for="password">Пароль</label>
        <br>
        <input type="password" id="password" name="password">
      </div>
      <button type="submit">Войти</button>
    </form>
  </div>
</template>

<script>
  export default {
    name: "LoginForm",
    data() {
      return {
        csrfToken: ""
      }
    },
    beforeMount() {
      this.csrfToken = this.$cookies.get("csrftoken")
    }
  }
</script>

<style lang="less" scoped>
  .form {
    margin: 150px auto;
    text-align: center;
    border: 2px solid #087e8b;
    border-radius: 10px;
    width: 300px;
    height: 260px;
    background-color: #ffffff;

    p {
      font-size: 24px;
      margin-top: 20px;
      margin-bottom: 20px;
    }

    button {
      background-color: #087e8b;
      border: 2px solid #087e8b;
      border-radius: 5px;
      color: #ffffff;
      margin-top: 20px;
      font-size: 18px;
      width: 100px;
      height: 36px;
      outline: none;
      transition: ease .8s;

      &:hover {
        background-color: #ffffff;
        color: #087e8b;
      }
    }
  }
</style>
