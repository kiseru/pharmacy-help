<template>
  <transition name="menu">
    <aside v-if="menu.showMenu">
      <ul class="sidebar-nav">
        <li class="sidebar-brand">
          <p>{{ user.first_name }} {{ user.last_name }}</p>
        </li>
        <li v-for="item in menuItems">
          <a v-bind:href="item.url">{{item.text}}</a>
        </li>
      </ul>
    </aside>
  </transition>
</template>

<script>
  import axios from 'axios'
  export default {
    name: "Menu",
    data() {
      return {
       /* user: {
          first_name: "",
          last_name: "Not found"
        }*/
       //user: this.$store.state.user
      }
    },
    computed: {
      user(){
        return this.$store.getters.getUser;
      }
    },
    props: {
      menu: {
        type: Object,
        required: true
      },
      menuItems: {
        type: Array,
        required: true
      }
    },
    beforeMount() {
      if (this.$store.state.user.first_name == ""){
        axios.get("/api/user")
         .then(
           response => {
             //this.user = response.data;
             this.$store.commit("setUser", response.data);
             console.log(this.$store.state.user)
           },
           error => console.log(error)

         );
      }

     }
  }
</script>

<style lang="less" scoped>
  aside {
    margin-top: 56px;
    position: fixed;
    top: 0;
    left: 0;
    width: 250px;
    background: #343a40;
    height: 100%;
    z-index: 2;
  }

  .sidebar-nav {
    list-style: none;
    padding-left: 0;

    li {
      text-indent: 20px;
      line-height: 40px;

      a {
        display: block;
        text-decoration: none;
        color: #999999;

        &:hover {
          text-decoration: none;
          color: #fff;
          background-color: rgba(255, 255, 255, 0.2);
        }

        &:active, &:focus {
          text-decoration: none;
        }
      }
    }

    .sidebar-brand {
      height: 65px;
      font-size: 18px;
      line-height: 60px;

      p {
        color: #999999;

        &:hover {
          color: #fff;
          background: none;
        }
      }
    }
  }

  .menu-enter-active, .menu-leave-active {
    transition: all .8s cubic-bezier(.65, .05, .36, 1);
  }

  .menu-enter {
    left: -100%;
  }

  .menu-leave-to {
    left: -100%;
  }


</style>
