(function() {
	var SFDing = {
		//url是encodeURIComponent(当前访问url后的值)
		config : function(url, callback, jsApiList){
			if(url == null || url == ""){
				url = encodeURIComponent(window.location.href);
			}
			if(jutil.isDing()){
				jsApiList = jsApiList == null ? ['device.geolocation.get'] : jsApiList;
				$.get("website/api/ding/jsapi/info", "url="+url, function(data){
					var isDingConfig = false;
					if(data != null && jutil.isNotEmpty(data.signature) && jutil.isNotEmpty(data.agentId) && jutil.isNotEmpty(data.corpId)){
						isDingConfig = true;
						dd.config({
							  debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
							  agentId: data.agentId, // 必填，应用的唯一标识
							  corpId: data.corpId, // 必填，企业的唯一标识
							  timeStamp: data.timestamp, // 必填，生成签名的时间戳
							  nonceStr: data.nonceStr, // 必填，生成签名的随机串
							  signature: data.signature,// 必填，签名
							  jsApiList: jsApiList // 必填，需要使用的JS接口列表
						});
						dd.error(function (err) {
							alert('dd error: ' + JSON.stringify(err));
						});//该方法必须带上，用来捕获鉴权出现的异常信息，否则不方便排查出现的问题
					}
					jutil.callFunc(callback, isDingConfig);
				});
			} else {
				jutil.callFunc(callback, false);
			}
		}		
	}
	
	if (!window.SFDing) {
		window.SFDing = SFDing;
	}
})();