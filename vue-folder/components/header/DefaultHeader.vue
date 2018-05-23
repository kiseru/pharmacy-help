<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <span class="navbar-brand">Pharmacy Help</span>
  </nav>
</template>

<script>
  export default {
    name: "DefaultHeader"
  }
</script>

<style lang="less" scoped>
  nav {
    height: 56px;
    padding: 0 16px 8px 0;
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    right: 0;

    .navbar-brand {
      margin-left: 16px;
    }
  }
</style>
