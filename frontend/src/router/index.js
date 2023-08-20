import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/thanks",
    name: "thanks",
    component: () => import("../views/ThanksView.vue"),
  },
  {
    path: "/screen",
    name: "screen",
    component: () => import("../views/ScreenView.vue"),
  },
  {
    path: "/images",
    name: "images",
    component: () => import("../views/ImagesView.vue"),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
