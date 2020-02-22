import axios from 'axios'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

export function sendData(image, render_host_image) {
	// 向服务器端传递数据
	axios({
	  method: 'post',
	  url: window.baseURL + '/api/encode',
	  data: image,
	  timeout: 500000,
	  crossDomain: true
	})
	.then((res) => {
	  render_host_image(res)
	})
	.catch((err) => {
	  console.log('axios failed', err)
	});
}

export function sendQRData(qrcode_data, render_host_image) {
	// 向服务器端传递数据
	axios({
	  method: 'post',
	  url: window.baseURL + '/api/qrcode',
	  data: qrcode_data,
	  timeout: 500000,
	  crossDomain: true
	})
	.then((res) => {
	  render_host_image(res)
	})
	.catch((err) => {
	  console.log('axios failed', err)
	});
}
