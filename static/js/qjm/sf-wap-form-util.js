(function() {
	var SFWapFormUtil = {
			loadCheckList : function(json){
	    		json = json || {};
	    		var eleId = json.id;
	    		//当url为空时，默认是字典，如果isDict是false，则默认是业务字典
	    		//如果是字典，则json.table = 
	    		var isDict = jutil.getValue(json.isDict, true);
	    		var isCheckbox = jutil.getValue(json.isCheckbox, true);
	    		var url = json.url;
	    		if(jutil.isEmpty(url)){
	    			url = isDict ? "content/json/dict/dm/"+json.table : "content/json/businessdict/"+json.pre+"/"+json.table;
	    		}
	    		var callback = json.callback;
				$.get(url, json.param, function(res){
					$("#"+eleId).empty();
					var name = eleId;
					for(var i in res){
						var dm = res[i].DM || res[i].dm;
						var mc = res[i].MC || res[i].mc; 
						var ck = res[i].CK || res[i].ck; 
						var redflag = res[i].REDFLAG || res[i].redflag; 
						var id = name+"_"+dm;
						var checked = ck == "1" ? "checked" : "";
						var disabled = redflag == "1" ? "disabled" : "";
						var checkBoxStype = isCheckbox ? "mui-checkbox" : "mui-radio";
						$("#"+eleId).append('<div class="mui-input-row radio-row '+checkBoxStype+' mui-left"><label>'+mc+'</label><input id="'+id+'" name="'+name+'" type="'+(isCheckbox ? "checkbox" : "radio")+'" value="'+dm+'" '+checked+' '+disabled+'/></div>');
					}
					if(callback){
						jutil.callFunc(callback);
	                }
				});
			},
		//测试发现，使用ajax异步动态获取数据后调用此方法生成开关会点击没反应，如果要用ajax，只能使用同步调用
		createSwitch : function(parentId, inputId, defaultValue, onclick){
			var active = "";
			if(defaultValue != null && (defaultValue == "1" || defaultValue == "Y" || defaultValue == "true" || defaultValue == true)){
				active = "mui-active";
			}
			if($("#"+inputId).length == 0){
				$("#"+parentId).append('<input type="hidden" id="'+inputId+'" name="'+inputId+'" value="'+(active=="mui-active"?"1":"0")+'"/>');
			}
			//mui-switch-mini
			$("#"+parentId).append('<div class="mui-switch mui-switch-mini '+active+'" id="'+inputId+'_switch"><div class="mui-switch-handle"></div></div>');
			$("#"+inputId+"_switch").on("tap", function(){
				if($(this).hasClass("mui-active")){
					$("#"+inputId).val("1");
				} else {
					$("#"+inputId).val("0");
				}
				jutil.callFunc(onclick, inputId);
			});
		},
		setSwitch : function(inputId, value, triggerClickEvent){
			if(value != null && (value == "1" || value == "Y" || value == "true" || value == true)){
				$("#"+inputId + "_switch").addClass("mui-active");
				$("#"+inputId).val("1");
				//不设置此样式的话，在首次页面打开时没问题，在之后如果多次反复设值时，样式会不对
				$(".mui-switch-handle", $("#"+inputId + "_switch")).css("transform", "translate(16px, 0px)");
			} else {
				$("#"+inputId + "_switch").removeClass("mui-active");
				$("#"+inputId).val("0");
				$(".mui-switch-handle", $("#"+inputId + "_switch")).css("transform", "translate(0px, 0px)");
			}
			if(triggerClickEvent){
				$("#" + inputId + "_switch").trigger("tap");
			}
		},
		switchClick : function(inputId, onclick){
			$("#"+inputId+"_switch").on("tap", function(){
				jutil.callFunc(onclick, inputId);
			});
		},
		resetValidator : function(formId){
			try{
				$("#"+formId).data('bootstrapValidator').resetForm(false);
			}catch(e){}
		},
		fillForm : function(data, formId){
            if(data){
                for (var key in data) {
                    var $element = $("#" + key);
                    if(jutil.isNotEmpty(formId) && $("#"+formId).length > 0){
                        $element = $("#" + key, $("#"+formId));
                    }
                    try {
                        var attrName = $element.attr("name");
                        var eType = $element.attr("type");
                        if (attrName) {
                        	if(eType != "checkbox" && eType != "radio"){
                        		if (attrName.indexOf(".") == -1) {
                                    $element.val(data[key]);
                                } else {
                                    var namearr = attrName.split(".");
                                    $element.val(data[namearr[0]][namearr[1]]);
                                }
                        	}
                        }
                    } catch (e) {
                    }
                }
            }
        }
	}
	
	if (!window.SFWapFormUtil) {
		window.SFWapFormUtil = SFWapFormUtil;
	}
})();