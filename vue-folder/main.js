import Vue from "vue";
import VueCookies from "vue-cookies";
import VueRouter from "vue-router";
import Vuex from "vuex";
import routes from "./routes";
import App from "./App.vue";
import axios from "axios/index";

Vue.config.productionTip = false;

Vue.use(VueCookies);
Vue.use(VueRouter);
Vue.use(Vuex);

const router = new VueRouter({
  mode: 'history',
  routes: routes
});

const store = new Vuex.Store({
  getters: {
    getUser: () => {
      let user = { first_name: "", last_name: "Not found" };
      axios.get("/api/user")
        .then(response => user = response.data);
      return user;
    }
  },
  mutations: {
    changeSearchText(state, text) {
      state.searchText = text;
    }
  },
  state: {
    searchText: ""
  }
});

new Vue({
  render: h => h(App),
  router,
  store
}).$mount("#app");
