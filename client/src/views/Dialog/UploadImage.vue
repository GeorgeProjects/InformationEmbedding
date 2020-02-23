<template>
	<div id = 'image-dialog'>
		<div class = "content-container">
			<el-upload
			  action="https://jsonplaceholder.typicode.com/posts/"
			  :http-request="getFile"
			  list-type="picture-card"
			  :on-preview="handlePreview"
			  :on-remove="handleRemove"
			  :before-upload="onBeforeUpload"
			  :file-list="fileList"
			  :auto-upload="true">
			    <i slot="default" class="el-icon-plus"></i>
			    <div slot="file" slot-scope="{file}">
			      <img
			        class="el-upload-list__item-thumbnail"
			        :src="file.url" alt="" 
			        :updateImageKey="updateImageKey">
			      <span class="el-upload-list__item-actions">
			      	<span
			          class="el-upload-list__item-preview"
			          @click="handlePictureSelection(file)">
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
			          @click="handleRemove(file, fileList)">
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
       disabled: false,
       updateImageKey: 0
   	  }	
	},
	watch: {
	},
	props: {
		updateImagePreviewUrl: {
			default: Function
		},
		closeUploadImageDialog: {
			default: Function
		},
		updateImagePreviewDialogVisible: {
			default: Function
		},
		decodeDataFromImage: {
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
		handlePreview: function(file) {
			console.log(file)
		},
		getFile: function() {
			console.log('upload file ok')
		},
		onBeforeUpload: function(file) {
			let self = this
			const isJPG = file.type === 'image/jpeg'
			const isPNG = file.type === 'image/png'
			if ((!isJPG) && (!isPNG)) {
			  let message = 'The uploaded image must be JPG or PNG format.'
			  this.promptMessage('error', message)
	          return false
	        }
	        if (this.fileList.map(function(e){ return e.name }).indexOf(file.name) !== -1) {
	           let message = 'The uploaded image has existed.'
	           this.promptMessage('error', message)
	           return false
	        }
	        var reader = new FileReader();
	        reader.onload = function () {
	            let fileName = file.name
	    		let fileIndex = self.fileList.map(function(e){ return e.name }).indexOf(file.name)
	    		if (fileIndex !== -1) {
			        self.fileList[fileIndex].url = reader.result
			        self.updateImageKey = (self.updateImageKey + 1) % 2
	    		}
	        }
	        self.fileList.push({
		        name: file.name
		    })
	        reader.readAsDataURL(file)
		},
		handleRemove(file, fileList) {
	    	let fileIndex = this.fileList.map(function(e){ return e.name }).indexOf(file.name)
	    	if (fileIndex !== -1) {
	    		this.fileList.splice(fileIndex, 1)
	    		this.promptMessage('success', 'Remove this image successfully!')
	    	} else {
	    		this.promptMessage('error', 'You cannot remove this image!')
	    	}
	    },
	    handlePictureSelection: function(file) {
	    	this.closeUploadImageDialog()
	    	this.decodeDataFromImage(file)
	    },
	    handlePictureCardPreview(file) {
	        this.updateImagePreviewUrl(file.url);
	        this.updateImagePreviewDialogVisible(true)
	    },
	    handleDownload(file) {
	    	console.log('this.fileList', this.fileList)
	    	let fileIndex = this.fileList.map(function(e){ return e.name }).indexOf(file.name)
	    	if (fileIndex !== -1) {
	    		var download = document.createElement('a');
				download.href = this.fileList[fileIndex].url
				download.download = this.fileList[fileIndex].name
				download.click();
	    	} else {
	    		this.promptMessage('error', 'The image file is empty.')
	    	}
	    },
		addDataCallback: function(resData) {
			this.promptMessage(resData.type, resData.message)
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
