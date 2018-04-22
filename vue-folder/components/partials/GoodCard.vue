<template>
  <div class="good-card card bg-light mb-3">
    <div class="card-body">
      <div class="card-title">{{medicine.name}}</div>
      <div class="card-subtitle mb-2 text-muted">{{medicine.type}}</div>
      <div class="card-text">{{medicine.description}}</div>
    </div>
    <div class="card-footer">
      <small>{{medicine.count}} шт.</small>
      <small>{{medicine.price}} &#x20bd;</small>
    </div>
    <!--<h3>{{ medicine.name }}</h3>-->
    <!--<p>{{ medicine.description }}</p>-->
    <!--<p>{{ medicine.type }}</p>-->
    <!--<div class="medicine-info">-->
      <!--<div class="medicine-count">{{ medicine.count }} шт.</div>-->
      <!--<div class="medicine-price">{{ medicine.price }} &#x20bd;</div>-->
    <!--</div>-->
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
    border: 2px solid #0062cc;
    margin: 10px auto;
    border-radius: 5px;
    text-align: center;

    .card-footer {
      background-color: rgba(0, 98, 204, 0.2);
    }
  }
</style>
