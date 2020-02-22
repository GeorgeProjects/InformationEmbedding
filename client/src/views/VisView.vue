<template>
	<div class = "vis-view">
		<div class = "vis-title-view">
			<VisTitleView :title="VisPanel" 
				:download="downloadImage">
			</VisTitleView>
		</div>
		<div class = "vis-content-view" v-if="displayMode==='vis'">
			<vega-lite :spec="specFromImage" v-if="showVisImage"></vega-lite>
		</div>
		<div class = "img-content-view" v-if="displayMode==='image'">
			<img id="host-image" :style="styleObject" :src="imageSrc" v-if="showImage"/>
		</div>
	</div>
</template>
<script>
	import { mapState, mapMutations } from 'vuex';
	import VisTitleView from './VisViewTitle.vue' 	
	import schema from 'vega-lite/build/vega-lite-schema.json';
	import vegaEmbed from 'vega-embed'
	import {mapVegaLiteSpec} from 'vue-vega'
	import VueVega from 'vue-vega'
	import { saveSvgAsPng, svgAsPngUri, svgAsDataUri } from 'save-svg-as-png'
	import { sendData } from '@/communication/sender.js'
	var PNGImage = require('pngjs-image');

	export default {
		name: "VisView",
		props: {
			specFromImage: {
				default: Object
			}
		},
		data() {
			return {
				imageSrc: "",
				showImage: false,
				showVisImage: false,
				CHART_PADDING: 64,
				VisPanel: "Visualization Panel",
				styleObject: {
					width: '100%'
				},
				displayMode: 'vis'
			}
		},
		components: {
			VisTitleView
		},
		computed: {
		},
		watch: {
		},
		mounted() {
		  let self = this
		  let visPanelWidth = $('.vis-content-view').width()
		  let visPanelHeight = $('.vis-content-view').height()
		  self.addChartSize(self.specFromImage, visPanelWidth, visPanelHeight)
		  self.showVisImage = true
		  setTimeout(function() {
		  		console.log('save results as png')
				self.saveResultAsPng()
		  }, 2000)
		},
		methods: {
			downloadImage: function() {

			},
			addChartSize: function(chartSpec, visPanelWidth, visPanelHeight) {
		      let padding = this.CHART_PADDING
		      if ('vconcat' in chartSpec) {
		        let viewNum = chartSpec['vconcat'].length
		        let singleViewHeight = (visPanelHeight - padding * 2) / viewNum
		        let singleViewWidth = visPanelWidth - padding * 2
		        for (let i = 0;i < viewNum;i++) {
		          chartSpec['vconcat'][i]['width'] = singleViewWidth
		          chartSpec['vconcat'][i]['height'] = singleViewHeight         
		        }
		      } else if ('hconcat' in chartSpec) {
		        let viewNum = chartSpec['hconcat'].length
		        let singleViewWidth = (visPanelWidth - padding * 2) / viewNum
		        let singleViewHeight = visPanelHeight - padding * 2
		        for (let i = 0;i < viewNum;i++) {
		          chartSpec['hconcat'][i]['width'] = singleViewWidth
		          chartSpec['hconcat'][i]['height'] = singleViewHeight         
		        }
		      } else {
		        let singleViewWidth = (visPanelWidth - padding * 2)
		        let singleViewHeight = visPanelHeight - padding * 2
		        chartSpec['width'] = singleViewWidth
		        chartSpec['height'] = singleViewHeight
		      }
		    },
			saveResultAsPng: function() {
				let self = this
				let svgElementArray = document.getElementsByClassName("marks")
				let dataAndSpec = {}
				if (svgElementArray.length > 0) {
					let svgElement = svgElementArray[0]
					// saveSvgAsPng(svgElement, "diagram.png");
					let image = new Image(); 
					var imageOperateCanvas = document.createElement('canvas');
					svgAsPngUri(svgElement).then(uri => {
						image.src = uri;
						dataAndSpec.image_uri = uri
						dataAndSpec.spec_data = self.specFromImage
						let dataAndSpecStr = JSON.stringify(dataAndSpec)
						sendData(dataAndSpecStr, self.render_host_image)
					});
					// var ctx = imageOperateCanvas.getContext("2d");
					// ctx.putImageData(imgData, 0, 0);
					svgAsDataUri(svgElement).then(uri => {
						// let png = new PNG({ filterType:4 }).parse(uri, function(error, data) {
						//     console.log(error, data)
						// });
						PNGImage.loadImage(uri, function(error, image) {
							console.log('image width', image.getWidth())
							console.log('image height', image.getHeight())							
						})
					})
				}
			},
			// render results
			render_host_image: function(res) {
				let hostImageStr = res.data
				let hostImageUri = 'data:image/png;base64,' + hostImageStr
				this.imageSrc = hostImageUri
				let imageWidth = +$('.vis-content-view').width()
				if (typeof(imageWidth) === 'undefined') {
					imageWidth = +$('.img-content-view').width()
				}
				this.styleObject.width = imageWidth + 'px'
				console.log('show host image')
				this.showImage = true	
			},
			...mapMutations([
		      ''
		    ])
		}
	}
</script>
<style scoped lang="less">
  	@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
	.vis-view {
		position: absolute;
		left: 0%;
		top: 0%;
		width: 100%;
		height: 100%;
		.vis-title-view {
			position: absolute;
            top: 0%;
            height: 2rem;
            left: 0%;
            width: 100%;
            border-bottom: @border-style;
		}
		.vis-content-view {
			position: absolute;
            top: calc(2.5rem + 1%);
            bottom: 2.5%;
            left: 2.5%;
            width: 95%;
		}
		.img-content-view {
			position: absolute;
            top: calc(2.5rem + 1%);
            bottom: 2.5%;
            left: 2.5%;
            width: 95%;
		}
	}
</style>