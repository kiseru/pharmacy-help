<template>
  <div id="user-info">
    <p>{{ user.first_name }}</p>
    <p>{{ user.last_name }}</p>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: "MenuUserInfo",
    data() {
      return {
        user: null
      }
    },
    beforeMount() {
      axios.get("/api/user")
        .then(
          response => this.user = response.data,
          error => this.user = { first_name: "Not found", last_name: "Not found" }
        );
    }
  }
</script>

<style scoped>
  #user-info {
    background-color: #f5f5f5;
    width: inherit;
    height: 150px;
    padding-top: 75px;
  }

  #user-info p {
    color: #3C3C3C;
    font-size: 22px;
    text-align: left;
    margin-left: 10px;
    margin-bottom: 1px;
  }
</style>
