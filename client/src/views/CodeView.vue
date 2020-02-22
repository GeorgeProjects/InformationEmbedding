<template>
	<div class = "code-view">
		<div class = "code-title-view">
			<TitleView :title="CodePanel" :download="downloadCode"></TitleView>
		</div>
		<div class = "code-content-view">
			<div class = "code-inner-content-view">
				<vue-json-pretty 
		            selectableType="single"
		            :data="specFromImageWithoutData"
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
		name: "CodeView",
		props: {
			specFromImage: {
				default: Object
			}
		},
		data() {
			return {
				CodePanel: "Code Panel",
				specFromImageWithoutData: {},
				treeDepth: 4
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
			let _specFromImage = JSON.parse(JSON.stringify(this.specFromImage))
			delete _specFromImage.data
			this.specFromImageWithoutData = _specFromImage
		},
		methods: {
			downloadCode: function(){
				console.log('downloadCode')
			}
		}
	}
</script>
<style>
	.vjs-tree {
		font-size: 12px;
	}
</style>
<style scoped lang="less">
  	@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
	.code-view {
		position: absolute;
		width: 100%;
		height: 100%;
		.code-title-view {
            position: absolute;
            top: 0%;
            height: 2rem;
            left: 0%;
            width: 100%;
            border-bottom: @border-style;
        }
        .code-content-view {
        	position: absolute;
            top: 2.1rem;
            bottom: 5px;
            left: 5px;
            right: 5px;
            text-align: left;
        	padding: 5px;
        	overflow-y: auto;
        	.code-inner-content-view {

        	}
        }
	}
</style>