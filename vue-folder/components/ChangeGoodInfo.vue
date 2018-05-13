<template>
  <div>
    <apothecary-header/>
    <change-good-form/>
  </div>
</template>

<script>
  import ChangeGoodForm from "./forms/ChangeGoodForm";
  import ApothecaryHeader from "./header/ApothecaryHeader";

  export default {
    name: "ChangeGoodInfo",
    components: {
      ChangeGoodForm,
      ApothecaryHeader
    }
  }
</script>

<style lang="less" scoped>

</style>
