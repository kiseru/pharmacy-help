import Vue from "vue";
import VueCookies from "vue-cookies";
import VueRouter from "vue-router";
import routes from "./routes";
import App from "./App.vue";

Vue.config.productionTip = false;

Vue.use(VueCookies);
Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  routes: routes
});

new Vue({
  render: h => h(App),
  router: router
}).$mount("#app");
