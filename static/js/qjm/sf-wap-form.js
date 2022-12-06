(function($){
    'use strict'
	//封装添加和修改的表单
    var SFWapForm = function(config){
    	config = config || {};
    	this.parentId = config.parentId;
    	this.key = config.key || "dm";//主键的name
    	this.keyValue = config.keyValue;//主键的值
    	this.formId = config.formId || 'form-edit';
    	//this.withReturnBtn = jutil.getValue(config.withReturnBtn, true);
    	this.btnHtml = config.btnHtml;
    	this.withOtherFlow = jutil.getValue(config.withOtherFlow, false);
    	this.bodyId = config.bodyId || "form_body";
    	this.saveBtnText = config.saveBtnText || "保存";
    	this.saveBtnId = config.saveBtnId || this.bodyId+'_save_btn';
    	this.title = config.title;
    	this.titleIsWarning = jutil.getValue(config.titleIsWarning, false);
    	this.init();
    	$("#"+this.formId+" input[type=text],textarea").each(function(){
    		if(jutil.isEmpty($(this).attr("placeholder")) && !$(this).is('[readonly]')){
    			$(this).attr("placeholder", "请填写");
    		}
    	});
    }
    
    SFWapForm.prototype.init = function(){
    	if(this.parentId){
    		var html = new Array();
			html.push('<div class="row">');
			html.push('  <div class="col-xs-12">');
			html.push('    <div class="content-box">');
			if(this.title){
				html.push('      <div id="'+this.formId+'_title" class="mui-ul-title '+(this.titleIsWarning?"text-red":"")+' '+(jutil.isEmpty(this.title)?"no-title":"")+'">');
				html.push('          <span>'+this.title+'</span>');
				html.push('      </div>');
			}else{
				html.push('      <div id="'+this.formId+'_title" class="mui-ul-title '+(this.titleIsWarning?"text-red":"")+'">');
				if(jutil.isEmpty(this.keyValue)){
					html.push('          <span>添加</span>');
				}else{
					html.push('          <span>修改</span>');
				}
				html.push('      </div>');
			}
			//form的padding-bottom默认为0，如果不设置padding-bottom为1px的话，里面的最后一个button的margin-bottom样式设置会无效，不能把form撑开
			html.push('      <form id="'+this.formId+'" class="form-horizontal mui-input-group" style="padding-bottom:1px">');
			html.push('        <div id="'+this.bodyId+'_box">');
			html.push('        </div>');
			//html.push(' <ul id="'+this.bodyId+'_box" class="mui-table-view mui-list-view mui-form"></ul>');
			/*html.push('        <div class="box-footer">');
			html.push('          <div class="text-center">');
			html.push('            <button type="submit" class="btn btn-primary" id="'+this.bodyId+'_save_btn">');
			html.push('              <i class="fa fa-save fa-lg"></i> 保存');
			html.push('            </button>');
			if(this.withReturnBtn){
				html.push('            <button type="button" class="btn btn-primary" id="'+this.bodyId+'_return_btn">');
				html.push('              <i class="fa fa-reply fa-lg"></i> 返回');
				html.push('            </button>');
			}
			html.push('          </div>');
			html.push('        </div>');*/
			if(this.btnHtml){
				//html.push('        <div class="box-footer">');
				//html.push('          <div class="text-center">');
				html.push(this.btnHtml);
				//html.push('          </div>');
				//html.push('        </div>');
			} else {
				html.push('          <button type="submit" class="btn btn-primary btn-xs mui-btn-block" style="'+(this.withOtherFlow?"margin-bottom: 0px;":"")+'" id="'+this.saveBtnId+'">'+this.saveBtnText+'</button>');
			}
			
			html.push('      </form>');
			html.push('    </div>');
			html.push('  </div>');
			html.push('</div>');
			$("#"+this.parentId).append(html.join(''));
			if($("#"+this.bodyId).length > 0){
				$("#"+this.bodyId+"_box").append($("#"+this.bodyId));
				$("#"+this.bodyId).removeClass("hidden");
			} else {
				$("#"+this.bodyId+"_box").append("<div id='"+this.bodyId+"'></div>");
			}
			
			if($("#operationType", $("#"+this.formId)).length == 0){
				var v = "Create";
				if(jutil.isNotEmpty(this.keyValue)){
					v = "Update";
				}
				$("#"+this.formId).append('<input type="hidden" name="operationType" id="operationType" value="'+v+'"/>');
	    	}
	    	//if($("#createTime", $("#"+this.formId)).length == 0){
	    	//	$("#"+this.formId).append('<input type="hidden" name="createTime" id="createTime"/>');
	    	//}
	    	if($("#"+this.key, $("#"+this.formId)).length == 0){
	    		var v = "";
				if(jutil.isNotEmpty(this.keyValue)){
					v = this.keyValue;
				}
	    		$("#"+this.formId).append('<input type="hidden" name="'+this.key+'" id="'+this.key+'" value="'+v+'"/>');
	    	}
	    	/*if(this.withReturnBtn){
	    		$("#"+this.bodyId+"_return_btn").on("tap", function(){
	  				jutil.goBack();
				});
	    	}*/
    	}
    }
    
    SFWapForm.prototype.titleVal = function(title){
    	if(title){
    		$("#"+this.formId+"_title").html(title);
    	}
    	return $("#"+this.formId+"_title").text();
    }
    
    SFWapForm.prototype.disableSave = function(disabled){
    	//不修改type会在validation触发时又激活按钮
    	if(disabled){
    		$("#"+this.saveBtnId).attr("type", "button");
    	} else {
    		$("#"+this.saveBtnId).attr("type", "submit");
    	}
		$("#"+this.saveBtnId).attr("disabled", disabled);
    }
    
    SFWapForm.prototype.createInputRow = function(id, name, label, required, beforeOrAfterOrParentId, placeType, placeholder, readOnly){
    	var input = '<div class="mui-input-row">';
    	input += '<label '+(required ? 'class="required"':'')+'>'+label+'</label>';
    	var ph = jutil.isEmpty(placeholder) ? '请填写' : placeholder;
    	if(readOnly){
    		ph = "";
    	}
    	input += '<input class="form-control" type="text" id="'+id+'" name="'+(jutil.isEmpty(name) ? id : name)+'" placeholder="'+(ph)+'" '+(readOnly ? "readonly":"")+'/>';
    	input += '</div>';
    	if(jutil.isEmpty(beforeOrAfterOrParentId)){
    		$("#"+this.bodyId).append(input);
    	} else {
    		if(placeType == "2"){
    			$("#"+beforeOrAfterOrParentId).before(input);
    		} else if(placeType == "3"){
    			$("#"+beforeOrAfterOrParentId).after(input);
    		} else {
    			$("#"+beforeOrAfterOrParentId).append(input);
    		}
    	}
    }
    
    SFWapForm.prototype.createSelectRow = function(id, valueId, valueName, label, required, beforeOrAfterOrParentId, placeType, placeholder){
    	var input = '<div class="mui-input-row">';
    	input += '<label '+(required ? 'class="required"':'')+'>'+label+'</label>';
    	input += '<input class="hidden" type="text" id="'+valueId+'" name="'+(jutil.isEmpty(valueName) ? valueId : valueName)+'" />';
    	input += '<input class="form-control" type="text" id="'+id+'" name="'+id+'" placeholder="'+(jutil.isEmpty(placeholder) ? '请选择' : placeholder)+'"/>';
    	input += '</div>';
    	if(jutil.isEmpty(beforeOrAfterOrParentId)){
    		$("#"+this.bodyId).append(input);
    	} else {
    		if(placeType == "2"){
    			$("#"+beforeOrAfterOrParentId).before(input);
    		} else if(placeType == "3"){
    			$("#"+beforeOrAfterOrParentId).after(input);
    		} else {
    			$("#"+beforeOrAfterOrParentId).append(input);
    		}
    	}
    }
    
    SFWapForm.prototype.createFileRow = function(id, label, required, beforeOrAfterOrParentId, placeType){
    	var input = '<div class="mui-input-row">';
    	input += '<label '+(required ? 'class="required"':'')+'>'+label+'</label>';
    	input += '<div id="'+id+'"></div> ';
    	input += '</div>';
    	if(jutil.isEmpty(beforeOrAfterOrParentId)){
    		$("#"+this.bodyId).append(input);
    	} else {
    		if(placeType == "2"){
    			$("#"+beforeOrAfterOrParentId).before(input);
    		} else if(placeType == "3"){
    			$("#"+beforeOrAfterOrParentId).after(input);
    		} else {
    			$("#"+beforeOrAfterOrParentId).append(input);
    		}
    	}
    }
    SFWapForm.prototype.createSwitchRow = function(id, label, required, defaultValue, onclick, beforeOrAfterOrParentId, placeType){
    	var active = "";
		if(defaultValue != null && (defaultValue == "1" || defaultValue == "Y" || defaultValue == "true" || defaultValue == true)){
			active = "mui-active";
		}
		
    	var input = '<div class="mui-input-row">';
    	input += '<label '+(required ? 'class="required"':'')+'>'+label+'</label>';
    	input += '<input type="hidden" id="'+id+'" name="'+id+'" value="'+(active=="mui-active"?"1":"0")+'"/> ';
    	input += '<div class="mui-switch mui-switch-mini '+active+'" id="'+id+'_switch"><div class="mui-switch-handle"></div></div>';
    	input += '</div>';
    	if(jutil.isEmpty(beforeOrAfterOrParentId)){
    		$("#"+this.bodyId).append(input);
    	} else {
    		if(placeType == "2"){
    			$("#"+beforeOrAfterOrParentId).before(input);
    		} else if(placeType == "3"){
    			$("#"+beforeOrAfterOrParentId).after(input);
    		} else {
    			$("#"+beforeOrAfterOrParentId).append(input);
    		}
    	}
    	
		$("#"+id+"_switch").on("tap", function(){
			if($(this).hasClass("mui-active")){
				$("#"+id).val("1");
			} else {
				$("#"+id).val("0");
			}
			jutil.callFunc(onclick, id);
		});
    }
    
    if (!window.SFWapForm) {
        window.SFWapForm = SFWapForm;
    }
})(jQuery);