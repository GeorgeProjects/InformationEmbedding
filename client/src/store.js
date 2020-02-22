import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    huahuhauhau: 'jaua'
  },
  mutations: {
    ['UPDATE'] (state, huahuhauhau) {
      console.log('huahuhauhau', huahuhauhau)
      console.log('state.huahuhauhau', state.huahuhauhau)
      state.huahuhauhau = huahuhauhau
      console.log('state.huahuhauhau', state.huahuhauhau)
    },
  },
  actions: {

  }
})
