<template>
  <div id="app">
    <el-menu
        class="el-menu-demo"
        mode="horizontal"
        background-color="#676767"
        text-color="#fff"
        :default-active="activeIndex"
        active-text-color="#ffd04b">
        <el-menu-item class='labelIcon' id="title">
          {{appName}}
        </el-menu-item>
        <el-menu-item index="upload" @click="upload_data">
          <i class="icon iconfont icon-upload"></i>       
        </el-menu-item>
        <el-menu-item index="qr_code" @click="generate_qr_code">
          <el-dropdown trigger="click" placement="bottom" :hide-on-click="false">
            <span class="el-dropdown-link">
              <i class="icon iconfont icon-Qr_code"></i><i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item class="block">
                <el-row>
                  <el-col :span="7">opacity</el-col>
                  <el-col :span="17">
                      <el-slider v-model="QRCodeOpacity" :step="1" :max="6" show-stops></el-slider>
                  </el-col>
                </el-row>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-menu-item> 
        <el-menu-item index="download_data" @click="download_data">
          <i class="icon iconfont icon-Datadownload"></i>
        </el-menu-item>
    </el-menu>
    <div class = "content-container">
      <div class = "vis-panel">
        <VisView :specFromImage="dynamicLinkChartSpec" ref="visview" v-if="showGroupBarChart"></VisView>
      </div>
      <div class = "dsl-panel">
        <CodeView :specFromImage="dynamicLinkChartSpec" v-if="showGroupBarChart"></CodeView>
      </div>
      <div class = "data-panel">
        <DataView :specFromImage="dynamicLinkChartSpec" v-if="showGroupBarChart"></DataView>
      </div>
    </div>
  </div>
</template>

<script>
import VisView from './views/VisView.vue'
import CodeView from './views/CodeView.vue'
import DataView from './views/DataView.vue'
import { mapVegaLiteSpec } from 'vue-vega'
import BarChartSpec from './assets/spec/vega-lite/bar.vl.json'
import population from './assets/spec/data/population.json'
import barley from './assets/spec/data/barley.json'
import cars from './assets/spec/data/cars.json'
import VueVega from 'vue-vega' 
import { sendQRData } from '@/communication/sender.js'
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'app',
  components: {
    VisView, CodeView, DataView
  },
  data() {
    return {
      appName: "Information Hiding",
      operationArray: [],
      activeIndex: '',
      showGroupBarChart: false,
      specFromImage: {},
      dataFromImage: {},
      QRCodeOpacity: 1,
      dynamicLinkChartSpec: {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "title": "cars",
        "background": "white",
        "vconcat": [
          {
            "mark": "point",
            "selection": {
              "brush": {
                "type": "interval",
                "init": {"x": [55, 160], "y": [13, 37]}
              }
            },
            "encoding": {
              "x": {"field": "Horsepower", "type": "quantitative"},
              "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
              "color": {
                "condition": {"selection": "brush", "field": "Cylinders", "type": "ordinal"},
                "value": "grey"
              },
              "tooltip": {"field": "Name", "type": "nominal"}
            },
            "transform": [{"filter": {"selection": "click"}}]
          },
          {
            "mark": "bar",
            "selection": {
              "click": {"type": "single", "encodings": ["x"]}
            },
            "encoding": {
              "x": {
                "field": "Year", 
                "type": "nominal",
                "axis": {"labelAngle": -40}
              },
              "y": {"aggregate": "count", "type": "quantitative"},
              "color": {
                "condition": {
                  "selection": "click",
                  "value": "steelblue"
                },
                "value": "grey"
              }
            },
            "transform": [{"filter": {"selection": "brush"}}]
          }
        ]
      }
    }
  },
  computed: {
    ...mapState([
      'displayMode'
    ])
  },
  watch: {
    displayMode: function() {
      console.log('displayMode', this.displayMode)
    }
  },
  methods: {
    iconClass(operation) {
      return 'icon-' + operation
    },
    upload_data: function() {

    },
    generate_qr_code: function() {
      this.$refs.visview.generate_qr_code()
    },
    download_data: function() {
    },
    sendQRData2Server: function() {
      let qrcode_data = "date precipitation temp_max temp_min wind weather 2012/01/01 0.0 12.8 5.0 4.7 drizzle 2012/01/02 10.9 10.6 2.8 4.5 rain 2012/01/03 0.8 11.7 7.2 2.3 rain 2012/01/04 20.3 12.2 5.6 4.7 rain 2012/01/05 1.3 8.9 2.8 6.1 rain 2012/01/06 2.5 4.4 2.2 2.2 rain 2012/01/07 0.0 7.2 2.8 2.3 rain 2012/01/08 0.0 10.0 2.8 2.0 sun 2012/01/09 4.3 9.4 5.0 3.4 rain 2012/01/10 1.0 6.1 0.6 3.4 rain 2012/01/11 0.0 6.1 -1.1 5.1 sun 2012/01/12 0.0 6.1 -1.7 1.9 sun 2012/01/13 0.0 5.0 -2.8 1.3 sun 2012/01/14 4.1 4.4 0.6 5.3 snow 2012/01/15 5.3 1.1 -3.3 3.2 snow"
      sendQRData(qrcode_data)
    }
  },
  mounted: function() {
    console.log('this.displayMode', this.displayMode)
    this.dynamicLinkChartSpec.data = {
      "values": cars
    }
    this.showGroupBarChart = true
    // this.sendQRData2Server()
  }
}
</script>

<style lang="less">
html {
  font-size: 100%;
}
@menu-height: 2.5rem;
@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  position: absolute;
  top: 0%;
  bottom: 0%;
  left: 0%;
  right: 0%;
  overflow: hidden;
  .el-menu.el-menu--horizontal {
    .el-menu-item {
      height: @menu-height;
      line-height: @menu-height;
    }
    .el-menu-item {
      border-bottom-color: rgb(84, 92, 100) !important;
      font-weight: bolder;
      font-size: 1rem;
      color: #dadada !important;
      padding: 0 10px;
      .icon {
        color: #dadada !important;
      }
      .el-icon-arrow-down.el-icon--right {
        color: #dadada !important;
      }
    }
    .el-divider--vertical {
      margin: 0 0;
    }
  }
  .labelIcon {
    font-size: 1rem;
  }
  .content-container {
    position: absolute;
    top: @menu-height;
    left: 0%;
    bottom: 0%;
    right: 0%;
    .vis-panel {
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 0%;
      right: 50%;
      border-right: @border-style;
    }
    .dsl-panel {
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 50%;
      right: 25%;
      border-right: @border-style;
    }
    .data-panel {
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 75%;
      right: 0%;
    }
  }
}
.el-dropdown-menu.el-popper {
  min-width: 240px;
  padding: 5px 0;
  .el-dropdown-menu__item {
    padding: 0 8px;
    .el-slider {
      .el-slider__button {
        width: 12px;
        height: 12px;
      }
    }
  }

}
</style>
