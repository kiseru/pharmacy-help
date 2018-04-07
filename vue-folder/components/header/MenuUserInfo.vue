<template>
  <div id="user-info">
    <p>Чехов</p>
    <p>Антон</p>
    <p>Павлович</p>
  </div>
</template>

<script>
  export default {
    name: "MenuUserInfo"
  }
</script>

<style scoped>
  #user-info {
    background-color: #f5f5f5;
    width: inherit;
    height: 150px;
    padding-top: 40px;
  }

  #user-info p {
    color: #3C3C3C;
    font-size: 22px;
    text-align: left;
    margin-left: 10px;
    margin-bottom: 1px;
  }
</style>