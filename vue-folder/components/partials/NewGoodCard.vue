<template>
  <a href="/apothecary/new">
    <div id="new-good-card" class="card">
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
    border: 2px solid #0062cc;
    margin: 10px auto;
    border-radius: 5px;
    text-align: center;
    transition: ease 0.8s;
    color: #0062cc;
  }

  #new-good-card .ion-ios-plus-outline {
    font-size: 70px;
    height: 96px;
    margin: 100px auto;
  }

  #new-good-card:hover {
    background-color: rgba(0, 98, 204, 0.8);
    border-color: rgba(0, 98, 204, 0.5);
    color: #f5f5f5;
  }
</style>
