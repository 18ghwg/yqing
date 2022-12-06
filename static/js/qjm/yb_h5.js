/**
 * Created by yiban on 16/5/23.
 *  author:liuchengbin
 *  desc:js<->oc js<->android
 */

/*
 函数名称：browser
 函数作用：判断访问终端
*/
var browser = {
    versions: function() {
        var u = navigator.userAgent,
        app = navigator.appVersion;
        return {
            mobile: !!u.match(/AppleWebKit.*Mobile.*/), //是否为移动终端
            ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端
            android: u.indexOf('Android') > -1 || u.indexOf('Adr') > -1, //android终端
            iPhone: u.indexOf('iPhone') > -1, //是否为iPhone或者QQHD浏览器
            iPad: u.indexOf('iPad') > -1, //是否iPad
        };
    }(),
    language: (navigator.browserLanguage || navigator.language).toLowerCase()
}

/*
 函数名称：getLocation
 函数作用：获取地理位置
 */
function gethtml5location_fun() {
    if(browser.versions.android) {
        //android 调用方式
        window.local_obj.yibanhtml5location();
    }else if(browser.versions.ios) {
        ios_yibanhtml5location();
    }else {
        onerror('该终端类型暂不支持使用');
    }
}

/*
 函数名称：yibanhtml5location
 函数作用：客户端获取地理位置，异步返回位置信息，html根据返回信息做界面内容处理
 参数说明：易班app回调设定，无需用户调用
    postion  Json  {"longitude":"经度坐标", "latitude":"纬度坐标", "address":"位置名称"}
 */
function yibanhtml5location(postion) {
    var editedHTML = document.getElementById("yibanhtml5");
    editedHTML.textContent = postion;
}

/*
 函数名称：phone
 函数作用：拨打电话
 参数说明：电话号码
 */
function phone_fun(num) {
    var pre = /^1\d{10}$/;
    var tre = /^0\d{2,3}-?\d{7,8}$/;
    if (pre.test(num) || tre.test(num)) {
        if(browser.versions.android) {
            //android 调用方式
            window.local_obj.phone(num);
        }else if(browser.versions.ios) {
            phone(num);
        }else {
            onerror('该终端类型暂不支持使用');
        }
    }else {
        onerror('手机号格式错误');
    }
}

/*
 函数名称：mail
 函数作用：发邮件
 参数说明：email地址
 */
function mail_fun(email) {
    var re = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/
    if(re.test(email)) {
        if(browser.versions.android) {
            //android 调用方式
            window.local_obj.mail(email);
        }else if (browser.versions.ios) {
            mail(email);
        }else {
            onerror('该终端类型暂不支持使用');
        }
    }else {
        onerror('邮箱地址格式错误');
    }
}

/*
 函数名称：encode
 函数作用：扫一扫
 */
function encode_fun() {
    if(browser.versions.android) {
        //android 调用方式
        window.local_obj.encode();
    }else if(browser.versions.ios) {
        encode();
    }else {
        onerror('该终端类型暂不支持使用');
    }
}

/*
 函数名称：getScanResult
 函数作用：扫一扫结果返回
 参数说明：二维码中必须包含“yiban_scan_result”标识，返回二维码字符串型内容；否则无该回调，直接以链接解析跳转
 */
function getScanResult(info) {
    document.getElementById("returnValue").value = info;
}

/*
 函数名称：back
 函数作用：返回app
 */
function back_fun() {
    if(browser.versions.android) {
        //android 调用方式
        window.local_obj.back();
    }else if(browser.versions.ios) {
        back();
    }else {
        onerror('该终端类型暂不支持使用');
    }
}

/*
 函数名称：download
 函数作用：下载
 参数说明：地址
 */
function download_fun(vurl) {
    if(browser.versions.android) {
        //android 调用方式
        window.local_obj.download(vurl);
    }else if(browser.versions.ios) {
        download(vurl);
    }else {
        onerror('该终端类型暂不支持使用');
    }
}

/*
 函数名称：photo
 函数作用：调用相册/拍照
 */
function photo_fun() {
    if(browser.versions.android) {
        //android 调用方式
        window.local_obj.camera();
    }else if (browser.platform.ios) {
        camera();
    }
}

/*
 函数名称：Q_camera_callback
 函数作用：相册/拍照结果回调
 参数说明：生成的图片地址
 */
function Q_camera_callback(info) {
    //根据实际情况可自行二次开发，原版基于方便测试用
    var result = eval('('+ info +')');
    document.getElementById("returnValue").value = result.o;
}

/*
 函数名称：onerror
 函数作用：非客户端的错误处理
 参数说明：errorInfo  错误信息
 */
function onerror(errorInfo) {
    //根据实际情况可自行二次开发，原版基于方便测试用
    var editedHTML = document.getElementById("yibanhtml5");
    editedHTML.textContent = errorInfo;
}

/*
 函数名称：mobile_api
 函数作用：调用客户端开放交互，传值详见相关交互说明
 参数说明：{action:"",params:{}}
 */
function mobile_api(jsonstr) {
    var tempJson = JSON.stringify(jsonstr);
    if(browser.versions.android) {
        //android 调用方式
        window.local_obj.js2mobile(tempJson);
    }else if(browser.versions.ios) {
        js2mobile(tempJson);
    }else {
        onerror('该终端类型暂不支持使用');
    }
}
/*
 函数名称：onlyid_back
 函数作用：返回设备相对唯一标示码
 参数说明：易班app回调设定，无需用户调用
    result  字符串
 */
function onlyid_back(result) {
    //根据实际情况可自行二次开发，原版基于方便测试用
    var editedHTML = document.getElementById("yibanhtml5");
    editedHTML.textContent = result;
}
/*
 函数名称：device_back
 函数作用：返回设备信息
 参数说明：易班app回调设定，无需用户调用
    result  Json  {"action":"yiban_device", "value":{"appVersion":"易班app版本", "deviceModel":"手机型号", "systemVersion":"手机系统版本"}}
 */
function device_back(result) {
    //根据实际情况可自行二次开发，原版基于方便测试用
    var editedHTML = document.getElementById("yibanhtml5");
    editedHTML.textContent = result;
}
