<template>
  <div class="form">
    <p>Добавить препорат</p>
    <form action="" method="post">
      <div>
        <input type="text">
      </div>

      <div>
        <input type="text">
      </div>

      <div>
        <input type="text">
      </div>

      <div>
        <input type="text">
      </div>

      <button type="submit">Добавить</button>
    </form>
  </div>
</template>

<script>
  export default {
    name: "AddGoodForm"
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