(function() {
	var SFWx = {
		//url是encodeURIComponent(当前访问url后的值)
		config : function(url, callback, jsApiList){
			if(url == null || url == ""){
				url = encodeURIComponent(window.location.href);
			}
			if(jutil.isWeiXin() || jutil.isWeiXinWork()){
				jsApiList = jsApiList == null ? ['getLocation','openLocation','scanQRCode'] : jsApiList;
				var jsapiUrl = "website/api/weixin/jsapi/info";
				if(jutil.isWeiXinWork()){
					jsapiUrl = "website/api/weixin/qy/jsapi/info";
				}
				$.get(jsapiUrl, "url="+url, function(data){
					var isWxConfig = false;
					if(data != null && jutil.isNotEmpty(data.signature) && jutil.isNotEmpty(data.appId)){
						isWxConfig = true;
						wx.config({
						      beta: true,// 企业号必须这么写，公众号没有这个参数，否则wx.invoke调用形式的jsapi会有问题
							  debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
							  appId: data.appId, // 必填，公众号的唯一标识/企业号的corpid
							  timestamp: data.timestamp, // 必填，生成签名的时间戳
							  nonceStr: data.nonceStr, // 必填，生成签名的随机串
							  signature: data.signature,// 必填，签名
							  jsApiList: jsApiList // 必填，需要使用的JS接口列表
						});
					}
					jutil.callFunc(callback, isWxConfig);
				});
			} else {
				jutil.callFunc(callback, false);
			}
		}		
	}
	
	if (!window.SFWx) {
		window.SFWx = SFWx;
	}
})();