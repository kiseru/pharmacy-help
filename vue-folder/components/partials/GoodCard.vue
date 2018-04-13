<template>
  <div class="good-card">
    <h3>{{ medicine.name }}</h3>
    <p>{{ medicine.description }}</p>
    <p>{{ medicine.type }}</p>
    <div class="medicine-info">
      <div class="medicine-count">{{ medicine.count }} шт.</div>
      <div class="medicine-price">{{ medicine.price }} &#x20bd;</div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "GoodCard",
    props: {
      medicine: {
        type: Object,
        required: true
      }
    }
  }
</script>

<style lang="less" scoped>
  .good-card {
    background-color: #ffffff;
    width: 200px;
    height: 300px;
    border: 2px solid #087E8B;
    margin: 10px auto;
    border-radius: 5px;
    text-align: center;

    .medicine-info {
      height: 50px;
      margin-top: 140px;
      font-size: 22px;

      .medicine-count {
        float: left;
        width: 50%;
        padding: 9px;
        border-right: 1px solid #087e88;
        border-top: 2px solid #087e88;
      }

      .medicine-price {
        float: right;
        width: 50%;
        padding: 9px;
        border-left: 1px solid #087e88;
        border-top: 2px solid #087e88;
      }
    }
  }
</style>
