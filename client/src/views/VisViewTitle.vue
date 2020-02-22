<template>
  <div class = "dsl-list-view-title">
    <span class = "text">{{title}}</span>
    <el-divider direction="vertical"></el-divider>
    <span class="icon iconfont icon-download" @click="download"></span>
    <span class="operation">
        <el-radio-group v-model="mode" @change="changeDisplayMode" size="mini">
          <el-radio-button label="vis"></el-radio-button>
          <el-radio-button label="image"></el-radio-button>
        </el-radio-group>
    </span>
  </div>
</template>

<script> 
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'DSLListTitle',
  props: {
    title: {
      type: String
    },
    download: {
      type: Function
    }
  },
  data() {
    return {
      mode: 'vis'
    }
  },
  created: function() {},
  beforeMount: function() {
  },
  mounted: function() {
  },
  watch: {
    displayMode: function() {
      //  更新在 visualization panel上选择的模式
      this.mode = this.displayMode
      console.log('change display mode')
    }
  },
  computed: { 
    ...mapState([
      'displayMode'
    ]) 
  },  
  methods: {
    changeDisplayMode: function() {
      console.log('changeDisplayMode', this.mode)
      this.UPDATE_DISPLAY_MODE(this.mode)
    },
    ...mapMutations([
      'UPDATE_DISPLAY_MODE'
    ])
  }
}
</script>
<style>
  .el-radio-button--mini .el-radio-button__inner {
    padding: 3px 4px !important;
  }
</style>
<style scoped lang="less">
  @border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
  .dsl-list-view-title {
    display: flex; 
    width: 100%; 
    height: 100%; 
    margin: auto; 
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    border-bottom: @border-style;
    .el-divider--vertical {
      margin-top: 0.5rem;
    }
    .iconfont {
      vertical-align: middle;
      margin-top: 0.4rem;
      margin-bottom:0.4rem;
      &:hover {
        background: lightgray;
      }
    }
    .operation {
      position: absolute;
      margin-top: 0.2rem;
      right: 5px;
    }
    .text {
       padding-left: 0.5rem;
       margin-left: 0; /* Important */ 
       margin-right: 0; /* Important */ 
       margin-top: auto; /* Important */ 
       margin-bottom: auto; /* Important */ 
       text-align: left;
       font-weight: bold;
    }
  }
</style>
