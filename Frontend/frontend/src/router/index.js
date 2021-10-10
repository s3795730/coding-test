import Vue from "vue";
import VueRouter from "vue-router";
import Orders from "../components/Orders.vue";
//bootstrap
import "bootstrap/dist/css/bootstrap.css";
//for pagination
import JwPagination from "jw-vue-pagination";
Vue.component("jw-pagination", JwPagination);

Vue.use(VueRouter);

//route for orders
const routes = [
  {
    path: "/orders",
    name: "Orders",
    component: Orders,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
