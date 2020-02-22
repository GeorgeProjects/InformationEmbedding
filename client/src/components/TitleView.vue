<template>
  <div class = "dsl-list-view-title">
    <span class = "text">{{title}}</span>
    <el-divider direction="vertical"></el-divider>
    <span class="icon iconfont icon-download" @click="download"></span>  
  </div>
</template>

<script> 
import { mapState, mapMutations } from 'vuex';

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
    }
  },
  created: function() {},
  beforeMount: function() {
  },
  mounted: function() {
  },
  watch: {
  },
  computed: {  
  },  
  methods: {
  }
}
</script>

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
    .icon-download {
      vertical-align: middle;
      margin-top: 0.4rem;
      margin-bottom:0.4rem;
      &:hover {
        background: lightgray;
      }
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
