<template>
  <a href="/medicines/new">
    <div id="new-good-card">
      <div class="ion-ios-plus-outline"></div>
    </div>
  </a>
</template>

<script>
  export default {
    name: "NewGoodCard"
  }
</script>

<style scoped>
  #new-good-card {
    background-color: #ffffff;
    width: 200px;
    height: 300px;
    border: 2px solid #087E8B;
    margin: 10px auto;
    border-radius: 5px;
    text-align: center;
    transition: ease 0.8s;
    color: #087e8b;
  }

  #new-good-card .ion-ios-plus-outline {
    font-size: 70px;
    height: 96px;
    margin: 100px auto;
  }

  #new-good-card:hover {
    background-color: #087e8b;
    color: #f5f5f5;
  }
</style>
