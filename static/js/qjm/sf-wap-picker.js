var SFWapPicker = (function (picker, $) {
    'use strict';
    //如需设置可选的开始日期和结束日期，可设置
    //{
	//	beginDate:new Date(),
	//	endDate: DateUtil.getDate(120, null)
	//}
    picker.normaldate = function(id, type, callback, config){
        $("#"+id).on('tap', function () {
        	var options = config;
        	if(options == null){
        		var optionsJson = this.getAttribute('data-options') || '{}';
                options = JSON.parse(optionsJson);
        	}
        	//默认只能选近10年，如果需要选更多，可设置config中的beginYear
			//默认改为从1940开始可选
			if(jutil.isEmpty(options["beginDate"])){
            	options["beginDate"] = new Date("1940-01-01");;
            }
            if(jutil.isEmpty(options["type"])){
            	options["type"] = type;
            }
            if($(this).val() != "" && jutil.isEmpty(options["value"])){
            	options["value"] = $(this).val();
            }
            var picker = new mui.DtPicker(options);
            picker.show(function (rs) {
                var timestr = rs.text;
                $('#'+id).val(timestr);
                picker.dispose();
                if(callback){
                    var _type = typeof callback ;
                    if (_type == "string") { 
                        eval(callback + "("+rs+")");  
                    } else if (_type == "function"){ 
                        callback(rs);
                    }
                }
            });
        });
    },
    //完整日期视图(年月日时分)
    picker.datetime = function(id, callback, config){
    	SFWapPicker.normaldate(id, "datetime", callback, config);
    	$("#"+id).val(DateUtil.currentDateTimeMin());
    },
    //年视图(年月日)
    picker.date = function(id, callback, config){
    	SFWapPicker.normaldate(id, "date", callback, config);
    	$("#"+id).val(DateUtil.currentDate());
    },
    //时间视图(时分)
    picker.time = function(id, callback, config){
    	SFWapPicker.normaldate(id, "time", callback, config);
    },
    //月视图(年月)
    picker.month = function(id, callback, config){
    	SFWapPicker.normaldate(id, "month", callback, config);
    	$("#"+id).val(DateUtil.currentYear() + "-" + DateUtil.currentMonth());
    },
    //时视图(年月日时)
    picker.hour = function(id, callback, config){
    	SFWapPicker.normaldate(id, "hour", callback, config);
    }
    return picker;
}(SFWapPicker||{}, jQuery));
