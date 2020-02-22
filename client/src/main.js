import Vue from 'vue'
import Vuex from 'vuex'

import App from './App.vue'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

import VueVega from 'vue-vega'
Vue.use(VueVega)

import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)
// import {VegaLiteComponent} from 'VegaLiteComponent'

// Vue.prototype.$axios = axios
window.baseURL = ""
if (process.env.NODE_ENV === 'production') {
  axios.defaults.baseURL = process.env.API_ROOT
  // 在production的模式下需要增加前缀
  window.baseURL = "http://vis.pku.edu.cn/gotree_server"
}

Vue.config.productionTip = false

import * as d3 from "d3"
window.d3 = d3

import * as $ from 'jquery'
window.$ = $

import './assets/font/iconfont.css'

new Vue({
  store,
  el: '#app',
  render: h => h(App)
})
