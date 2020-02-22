<template>
	<div id = 'image-dialog'>
		<div class = "content-container">
			<el-upload
			  action="#"
			  list-type="picture-card"
			  :auto-upload="false">
			    <i slot="default" class="el-icon-plus"></i>
			    <div slot="file" slot-scope="{file}">
			      <img
			        class="el-upload-list__item-thumbnail"
			        :src="file.url" alt="">
			      <span class="el-upload-list__item-actions">
			      	<span
			          class="el-upload-list__item-preview"
			          @click="handlePictureCardPreview(file)">
			          <span class="icon iconfont icon-xuanzhong"></span>
			        </span>
			        <span
			          class="el-upload-list__item-preview"
			          @click="handlePictureCardPreview(file)">
			          <i class="el-icon-zoom-in"></i>
			        </span>
			        <span
			          v-if="!disabled"
			          class="el-upload-list__item-delete"
			          @click="handleDownload(file)">
			          <i class="el-icon-download"></i>
			        </span>
			        <span
			          v-if="!disabled"
			          class="el-upload-list__item-delete"
			          @click="handleRemove(file)">
			          <i class="el-icon-delete"></i>
			        </span>
			      </span>
			    </div>
			</el-upload>
    	</div>
	</div>
</template>

<script>
  import { mapState, mapMutations } from 'vuex'
 
  export default {
	name: 'DataDialog',
	components: {},
	data() {
	  return {
       search: ' ',
       fileList: [],
       selectedTreeDataName: null,
       tempSelection: null,
       dialogImageUrl: '',
       dialogVisible: false,
       disabled: false
   	  }	
	},
	watch: {
	},
	props: {
		updateImagePreviewUrl: {
			default: Function
		},
		updateImagePreviewDialogVisible: {
			default: Function
		}
  	},
	created: function () {
	},
	mounted: function() {
	},
	computed: {
		...mapState([
	      'userInfoName'
	    ])
	},
	methods: {
		closeDataDialog: function() {
		},
		confirmSelection: function() {
		},
		onBeforeUpload: function(file) {
		},
		handlePreview: function(file) {
		},
		handleRemove(file) {
	    	console.log(file);
	    },
	    handlePictureCardPreview(file) {
	        this.updateImagePreviewUrl(file.url);
	        this.updateImagePreviewDialogVisible(true)
	    },
	    handleDownload(file) {
	        console.log(file);
	    },
		handleUploadSuccess: function(res, file) {
			console.log('upload success!')
		},
		addDataCallback: function(resData) {
			this.promptMessage(resData.type, resData.message)
		},
		handleRemove: function() {
		},
	    promptMessage: function(type, message) {
			this.$message({
              type: type,
              message: message
            })
		}
	}
  }
</script>
<style scoped lang="less">
  #image-dialog {
  	.content-container {
  		.iconfont {
  			font-size: 1.4rem;
  		}
  	}
  }
</style>
