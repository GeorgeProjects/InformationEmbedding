<template>
	<div class = "data-view">
		<div class = "data-title-view">
			<TitleView :title="DataPanel" :download="downloadData"></TitleView>
		</div>
		<div class = "data-content-view">
			<div class = "data-inner-content-view">
	          	<vue-json-pretty 
		            selectableType="single"
		            :data="dataFromImage"
		            :deep="treeDepth"
		            :showDoubleQuotes="false"
		            :highlightMouseoverNode="true"
		            :highlightSelectedNode="true"
		            :selectOnClickNode="true">
	          	</vue-json-pretty>	
          	</div>		
		</div>
	</div>
</template>
<script>
	import TitleView from '../components/TitleView.vue' 
	import VueJsonPretty from 'vue-json-pretty'
	export default {
		name: "DataView",
		props: {
			specFromImage: {
				default: Object
			}
		},
		data() {
			return {
				DataPanel: "Data Panel",
				treeDepth: 3,
				dataFromImage: {}
			}
		},
		components: {
			TitleView, VueJsonPretty
		},
		watch: {
		},
		computed: {
		},
		mounted() {
			this.dataFromImage = this.specFromImage.data
		},
		methods: {
			downloadData: function() {
				console.log('downloadData')
			}
		}
	}
</script>
<style scoped lang="less">
  	@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
	.data-view {
		position: absolute;
		width: 100%;
		height: 100%;
		.data-title-view {
            position: absolute;
            top: 0%;
            height: 2rem;
            left: 0%;
            width: 100%;
            border-bottom: @border-style;
        }
        .data-content-view {
        	position: absolute;
            top: 2.1rem;
            bottom: 5px;
            left: 5px;
            right: 5px;
            text-align: left;
            font-size: 0.8rem;
        	padding: 5px;
        	overflow-y: auto;
        }
	}
</style>