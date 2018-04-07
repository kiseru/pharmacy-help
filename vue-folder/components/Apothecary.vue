<template>
  <div>
    <apothecary-header/>
    <goods-cards/>
  </div>
</template>

<script>
  import ApothecaryHeader from "./header/ApothecaryHeader";
  import GoodsCards from "./partials/GoodsCards";
  
  export default {
    name: "Apothecary",
    components: {
      ApothecaryHeader,
      GoodsCards
    }
  }
</script>

<style scoped>

</style>