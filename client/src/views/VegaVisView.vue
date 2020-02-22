<template>
	<div class = "vega-vis-view">
		<vega-lite :spec="specFromImage"></vega-lite>
		<img id="host-image" :style="styleObject" :src="imageSrc" v-if="showImage"/>
	</div>
</template>
<script>
	import schema from 'vega-lite/build/vega-lite-schema.json';
	import vegaEmbed from 'vega-embed'
	import {mapVegaLiteSpec} from 'vue-vega'
	import VueVega from 'vue-vega'
	import { saveSvgAsPng, svgAsPngUri, svgAsDataUri } from 'save-svg-as-png'
	import { sendData } from '@/communication/sender.js'
	var PNGImage = require('pngjs-image');

	export default {
		name: "VegaVisView",
		props: {
			specFromImage: {
				default: Object
			}
		},
		data() {
			return {
				imageSrc: "",
				showImage: false,
				styleObject: {
					width: '100%'
				}
			}
		},
		components: {
		},
		watch: {
		},
		computed: {
		},
		mounted() {
		  let self = this
		  setTimeout(function() {
				self.saveResultAsPng()
		  }, 2000)
		},
		methods: {
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
						console.log('uri', uri)
						image.src = uri;
						dataAndSpec.image_uri = uri
						dataAndSpec.spec_data = self.specFromImage
						let dataAndSpecStr = JSON.stringify(dataAndSpec)
						sendData(dataAndSpecStr, self.render_host_image)
					});
					// ctx.putImageData(imgData, 0, 0);
					// svgAsDataUri(svgElement).then(uri => {
					// 	// let png = new PNG({ filterType:4 }).parse(uri, function(error, data) {
					// 	//     console.log(error, data)
					// 	// });
					// 	PNGImage.loadImage(uri, function(error, image) {
					// 		console.log('image width', image.getWidth())
					// 		console.log('image height', image.getHeight())							
					// 	})
					// })
				}
			},
			// render results
			render_host_image: function(res) {
				let hostImageStr = res.data
				let hostImageUri = 'data:image/png;base64,' + hostImageStr
				this.imageSrc = hostImageUri
				let imageWidth = $('.vega-vis-view .marks').width()
				this.styleObject.width = imageWidth + 'px'
				this.showImage = true	
			}
		}
	}
</script>
<style scoped lang="less">
	.vega-vis-view {
		position: absolute;
		width: 100%;
		height: 100%;
		.marks {
			background: white;
		}
	}
</style>