<template>
  <a v-bind:href="item.url">
    <div class="menu-list-item">
      {{ item.text }}
    </div>
  </a>
</template>

<script>
  export default {
    name: "MenuListItem",
    props: {
      item: {
        type: Object,
        required: true
      }
    }
  }
</script>

<style scoped>
  .menu-list-item {
    height: 50px;
    width: 250px;
    background-color: #f5f5f5;
    transition: ease 0.3s;
    padding: 12px 0;
  }

  .menu-list-item:hover {
    background-color: #087E8B;
    color: #f5f5f5;
  }

  a {
    color: #3C3C3C;
    font-size: 18px;
    margin: 0 auto;
    text-decoration: none;
    width: inherit;
  }
</style>