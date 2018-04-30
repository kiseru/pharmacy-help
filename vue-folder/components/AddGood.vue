<template>
  <div>
    <apothecary-header/>
    <add-good-form/>
  </div>
</template>

<script>
  import AddGoodForm from "./forms/AddGoodForm";
  import ApothecaryHeader from "./header/ApothecaryHeader";

  export default {
    name: "AddGood",
    components: {
      AddGoodForm,
      ApothecaryHeader
    }
  }
</script>

<style lang="less" scoped>

</style>
