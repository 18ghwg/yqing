(function($){
    'use strict'
	//封装查看详情
    var SFWapView = function(config){
    	config = config || {};
    	this.parentId = config.parentId;
    	this.title = config.title || "详情";
    	this.titleIsWarning = jutil.getValue(config.titleIsWarning, false);
    	this.showDetail = jutil.getValue(config.showDetail, true);
    	//以下参数与审批流程有关，不需要的可以不配置
    	this.isAuditFlow = jutil.getValue(config.isAuditFlow, false);//如果是自定义审批流程，则可配置为true，为true时需配置auditId和cddm
    	this.auditId = config.auditId;//类型是deal时，auditId是审核表的ID，类型是view时，auditId是申请表的ID
    	this.cddm = config.cddm;
    	this.auditType = config.auditType || SFWapView.AUDIT_TYPE_VIEW;
    	this.auditBackUrl = config.auditBackUrl;
    	this.sqid = null;//申请表的ID，在addAuditFlow时会自动设置
    	this.lxdm = null;//流向代码，在addAuditFlow时会自动设置
    	this.detailUrl = null;//自定义审批流程时，获取详情的Url，在addAuditFlow时会自动设置
    	//this.textWidth = config.textWidth || "75";
    	this.labelWidth = config.labelWidth || "110px";
    	this.init();
    }
    
    SFWapView.AUDIT_TYPE_DEAL = "deal";//可以办理
    SFWapView.AUDIT_TYPE_VIEW = "view";//仅查看进展
    
    SFWapView.prototype.init = function(clean){
    	if(this.parentId){
    		if(clean){
    			$("#"+this.parentId).empty();
    		}
    		if(this.showDetail){
    			var html = new Array();
        		var ulId = this.parentId+"_ul";
        		var style = jutil.isEmpty(this.title) ? "height:5px;padding:0px" : "";
    			html.push('<div class="mui-ul-title '+(this.titleIsWarning?"text-red":"")+'" style="'+style+'">');
    			html.push('  <span>'+this.title+'</span>');
    			html.push('</div>');
    			html.push('<ul class="mui-table-view mui-list-view" id="'+ulId+'">');
    			html.push('</ul>');
    			$("#"+this.parentId).append(html.join(''));
    		}
			
			if(this.isAuditFlow && jutil.isNotEmpty(this.auditId) && jutil.isNotEmpty(this.cddm)){
				this.addAuditFlow(this.auditId, this.cddm);
				if(jutil.isNotEmpty(this.detailUrl)){
					if(jutil.isNotEmpty(this.sqid)){
						if(this.auditType == SFWapView.AUDIT_TYPE_DEAL && (this.shzt == '0' || this.shzt == null)){
							this.addAuditDeal(ulId);
						}
					}
					var labelWidth = this.labelWidth.replace("px","");
		    		$.get(this.detailUrl, "ywid="+this.sqid, function(data){
		        		$("#"+ulId).append(data);
		        		//处理内容的宽度，图片的预览
		        		var ulWidth = $("#"+ulId).width();
		    			var inputWidth = ulWidth - labelWidth - 35 + "px";
		    			$("#"+ulId+" .mui-table-view-cell-text").css("width", inputWidth);
		    			$("#"+ulId+" .mui-table-view-cell-img").viewer({
		    				filter : function(selector) {    
		    			        // 选择器过滤
		    			        return selector.className.indexOf('ignore-view') > 0 ? false : true;    
		    			    } 
		    			});
		        	});
		    	} else {
		    		$("#"+ulId).append('<li class="mui-table-view-cell mui-table-view-cell-view text-red">流程已终止</li>');
		    	}
			}
    	}
    }
    
    SFWapView.prototype.hideRow = function(id){
    	var ids = id.split(",");
		for(var k in ids){
			$("#"+ids[k]+"_li").hide();
		}
	}
	
    SFWapView.prototype.showRow = function(id){
    	var ids = id.split(",");
		for(var k in ids){
			$("#"+ids[k]+"_li").show();
		}
	}
    
    SFWapView.prototype.createStuBase = function(stu, lcCode){
		this.createRow("xh_v", "学号", stu.xh);
		this.createRow("xm_v", "姓名", stu.xm);
		this.createRow("xb_v", "性别", stu.xb != null ? stu.xb.mc : "");
		this.createRow("bj_v", "班级", stu.szbj != null ? stu.szbj.bjmc : "");
		var that = this;
		$.ajax({
			url : "content/admin/config/sensitive/lxdh/show",
			type: "get", 
			cache:false, 
			async:false, 
			data:"lcCode="+lcCode,
         	success: function(show){ 
         		if(show == "1"){
    				that.createRow("sjhm_v", "联系电话", stu.sjhm);
    				that.createRow("lxrdh_v", "联系人电话", stu.lxrdh);
    			}
         	} 
		});
	}
    
    /**
     * label:标题，id:内容区的span的ID，width:span的宽度，text:span中的文本内容
     * dom是一段html，如果不存，则默认是span，一些地方需要显示图片或者链接的可以直接传dom进来
     */
    SFWapView.prototype.createRow = function(id, label, text, isLink, isImg, dom){
		this.createRow2({
			label:label,
			id:id,
			text:text,
			isLink:isLink,
			isImg:isImg,
			dom:dom
		});
    }
    
    //普通列表行
    SFWapView.prototype.createRow2 = function(json){
    	var label = json.label;
    	var id = json.id;
    	var text = json.text == null ? "" : json.text;//json.text || ""，如果text传进来是数字0，会变成空
    	var hasLabel = jutil.getValue(json.hasLabel, true);
    	var isLink = jutil.getValue(json.isLink, false);
    	var isImg = jutil.getValue(json.isImg, false);
    	var isBtn = jutil.getValue(json.isBtn, false);
    	var dom = json.dom;
    	var parent = json.parentId || this.parentId+"_ul";
    	var liId = id + "_li";
    	var labelId = id + "_label";
    	if(isLink && jutil.isNotEmpty(text)) {
			if(text.match(/\.(png|jpe?g|gif|svg|PNG|JPE?G|GIF|SVG)(\?.*)?$/)){
				isLink = false;
				isImg = true;
			}
		}
    	if($("#"+liId, $("#"+parent)).length == 0){
    		var html = new Array();
    		var ulWidth = $("#"+parent).width();
    		var fixWidth = isBtn ? 0 : 35;
			var inputWidth = hasLabel ? ulWidth - this.labelWidth.replace("px","") - fixWidth : ulWidth - fixWidth;
    		$("#"+parent).append('<li id="'+liId+'" class="mui-table-view-cell mui-table-view-cell-view '+(isBtn ? "mui-table-view-cell-btn" : "")+'"></li>');
    		if(hasLabel){
    			$("#"+liId).append(' <label id="'+labelId+'" style="width:'+this.labelWidth+';vertical-align: top;">'+label+'</label>');
    		}
    		if(isImg){
    			$("#"+liId).append(' <div id="'+id+'" style="margin-top:6px"></div>');
    		} else {
    			$("#"+liId).append(' <div id="'+id+'" style="display:inline-block;width:'+inputWidth+'px"></div>');
    		}
    	} else {
    		if(hasLabel){
    			$("#"+labelId).text(label);
    		}
    	}
    	if(dom){
			$("#" + id).html(dom);
		}else{
			if(isLink){
				$("#"+id).html(jutil.isEmpty(text) ? '' : '<a style="color:#007aff" href="'+text+'">下载</a>');
			} else if(isImg) {
				if(jutil.isNotEmpty(text)){
					if (typeof text != "string") {
						var hasImg = false;
						for(var i in text){
							var filePath = text[i].path;
							if(filePath.indexOf(".doc")>0){
								var img = '<a href="'+filePath+'" target="_blank"><img id="'+id+'_img_'+i+'" src="content/images/wps.png" class="weui-uploader__file ignore-view"/></a>';
			    				$("#"+id).append(img);
							} else {
								hasImg = true;
								var img = '<img id="'+id+'_img_'+i+'" src="'+text[i].path+'" class="weui-uploader__file" />';
			    				$("#"+id).append(img);
							}
						}
						if(hasImg){
							jutil.viewer($("#"+id));//看多张图片
						}
					} else {
						var img = '<img id="'+id+'_img" src="'+text+'" class="weui-uploader__file" />';
	    				$("#"+id).append(img);
	    				jutil.viewer($("#"+id));//看一张图片
					}
				} 
			} else {
				$("#"+id).html(text);
			}
		}
    }
    
    //带状态的行，类似审核的样式
    SFWapView.prototype.createStatusRow = function(parentId, label, content, ztmc, otherJson){
		var html = new Array();
		html.push("<li class='mui-table-view-cell'>");
		html.push("<div class='mui-table'>");
		html.push("  <div class='mui-table-cell'>");
		html.push("  <div class='mui-ellipsis-2 mui-table-view-cell-gap'>"+label+"</div>");
		if(content.indexOf("<p") > -1){
			html.push(content);
		}else{
			html.push("  <p class='mui-ellipsis'>"+content+"</p>");
		}
		html.push("  </div>");
		html.push("</div>");
		if(!jutil.isEmpty(ztmc)){
			html.push(SFWapListUtil.loadBadge(ztmc));
		}
		html.push("</li>");
		$("#"+parentId).append(html.join(''));
    }
    
    SFWapView.prototype.fillValue = function(data){
        if(data){
            for (var key in data) {
                var $element = $("#" + key);
                try {
                    var eType = $element.attr("type");
                	if(eType != "checkbox" && eType != "radio"){
                		$element.text(data[key] == null ? "" : data[key]);
                	}
                } catch (e) {
                }
            }
        }
    }
    
    SFWapView.prototype.removeFlow = function(id){
    	if($("#"+id+"_flow_box").length > 0){
    		$("#"+id+"_flow_box").remove();
    	}
    }
    
    SFWapView.prototype.addOtherFlow = function(title, id){
    	if(this.parentId){
    		var html = new Array();
    		if(title == null){
    			title = "";
    		}
    		var style = jutil.isEmpty(title) ? "height:5px;padding:0px" : "";
			html.push('<div id="'+id+'_flow_box"><div class="mui-ul-title" style="'+style+'">');
			html.push('  <span>'+title+'</span>');
			html.push('</div>');
			html.push('<ul class="mui-table-view mui-table-view-striped mui-table-view-condensed" id="'+id+'">');
			html.push('</ul></div>');
			$("#"+this.parentId).append(html.join(''));
    	}
    }
    
    SFWapView.prototype.addAuditFlow = function(sqid, cddm){
    	if(this.parentId){
    		var html = new Array();
			html.push('<div id="'+sqid+'_flow_box"><div class="mui-ul-title">');
			html.push('  <span>进度</span>');
			html.push('</div>');
			html.push('<ul class="mui-table-view mui-table-view-striped mui-table-view-condensed" id="'+this.parentId+'_audit_ul">');
			html.push('</ul></div>');
			$("#"+this.parentId).append(html.join(''));
    	}
    	if(cddm == null){
    		cddm = "";
    	}
    	var that = this;
    	var async = this.isAuditFlow ? false : true;
    	var url = this.auditType == SFWapView.AUDIT_TYPE_DEAL ? "content/audit/audit/getAuditDetailsForDeal":"content/audit/audit/getAuditDetails";
    	$.ajax({
    		async:async,
    		url:url+"?_fqcddm_="+cddm+"&_id_="+sqid,
    		success:function(data){
    			if(jutil.isEmpty(data) || data.length == 0){
    				$("#"+sqid+"_flow_box").hide();
    				return;
    			}
        		for(var key in data){
        			var obj = data[key];
        			if(key == 0){
        				that.setDetailUrl(data[key].FQXXCDLJ);
        				that.setSqid(data[key].SQID);
        				that.setLxdm(data[key].LXDM);
        			}
        			if(data[key].DM == that.auditId){
        				that.setShzt(data[key].SHZT);
        			}
        			//var content = "<p class='mui-h6 mui-ellipsis'>审核结果：" + obj.SHZTMC;
        			var content = "";
        			var haveImg = false;
        			if(obj.SHSJ != null){
        				content += "<p class='mui-ellipsis mui-table-view-cell-gap'><i class='fa fa-clock-o' /> " + (obj.SHSJ == null ? "" : DateUtil.cutDateTimeMin(obj.SHSJ));
        				if(obj.SHOW_SHR_IND == "1"){
        					content += "<p style='width:80%'><i class='fa fa-user' /> " + obj.SHRXM;
        				}
        				if(jutil.isNotEmpty(obj.SHYJ)){
        					content += "<p style='width:80%'><i class='fa fa-file-text-o' /> " + obj.SHYJ;
        				}
        				if(obj.fileList != null){
        					content += '<div class="row" style="margin-top:5px;"><div class="col-xss-12" id="'+obj.DM+'_box">';
							for(var i in obj.fileList){
								if(obj.fileList[i].path.indexOf(".doc")>0){
									content += '<a href="'+obj.fileList[i].path+'" target="_blank"><img src="content/images/wps.png" class="weui-uploader__file"/></a>';
								} else {
									haveImg = true;
									content += '<img src="'+obj.fileList[i].path+'" class="weui-uploader__file" />';
								}
							}
        					content += "</div></div>";
        				}
        			}
        			var label = "第"+obj.BS+"步："+obj.LXMC;
        			that.createAuditRow(label, content, obj.SHZTMC);
        			if(obj.SHSJ != null && obj.fileList != null && haveImg){
        				jutil.viewer($("#"+obj.DM+"_box"));//看多张图片
        			}
        		}
    		}
    	});
    }
    
    SFWapView.prototype.createAuditRow = function(label, content, ztmc){
		var html = new Array();
		html.push("<li class='mui-table-view-cell'>");
		html.push("<div class='mui-table'>");
		html.push("  <div class='mui-table-cell'>");
		if(!jutil.isEmpty(ztmc)){
			html.push("  <div class='mui-ellipsis-2 mui-table-view-cell-gap'>"+label+"</div>");
		} else {
			html.push("  <div class='mui-ellipsis-2 mui-table-view-cell-gap disabled'>"+label+"</div>");
		}
		if(content.indexOf("<p") > -1){
			html.push(content);
		}else{
			html.push("  <p style='width:80%'>"+content+"</p>");
		}
		html.push("  </div>");
		html.push("</div>");
		if(!jutil.isEmpty(ztmc)){
			html.push(SFWapListUtil.loadBadge(ztmc));
		}
		html.push("</li>");
		$("#"+this.parentId+"_audit_ul").append(html.join(''));
    }
    
    /**
     * 审批办理
     */
    SFWapView.prototype.addAuditDeal = function(afterId){
    	if(afterId){
    		var ulId = this.parentId+'_audit_deal_ul';
    		var html = new Array();
			html.push('<div class="mui-ul-title">');
			html.push('  <span>办理</span>');
			html.push('</div>');
			html.push('<ul class="mui-table-view mui-table-view-striped mui-table-view-condensed" id="'+ulId+'">');
			html.push('</ul>');
			$("#"+afterId).after(html.join(''));
			
			html = new Array();
			html.push('<form action="" id="dealWithForm" method="post" class="form-horizontal mui-input-group">');
			html.push('  <input type="hidden" name="dm" id="dm" value="'+this.auditId+'" />');
			var ulWidth = $("#"+ulId).width();
			var inputWidth = ulWidth - this.labelWidth.replace("px","") - 65;
			html.push('  <div class="mui-input-row mui-input-row-in-view radio-row">');
			html.push('    <label style="width:'+this.labelWidth+'">审核结果</label>');
			html.push('    <input type="radio" id="shjg1" name="shjg" value="1" checked="checked" /><label for="shjg1">通过</label> ');
			html.push('    <input type="radio" id="shjg2" name="shjg" value="2" /><label for="shjg2">不通过</label> ');
			html.push('    <input type="radio" id="shjg3" name="shjg" value="3" /><label for="shjg3">退回</label> ');
			html.push('  </div>');
			html.push('  <div class="mui-input-row mui-input-row-in-view">');
			html.push('    <label style="width:'+this.labelWidth+'">审核意见</label>');
			html.push('    <textarea type="text" class="form-control" id="shyj" name="shyj" rows="2" style="width:'+inputWidth+'px"></textarea> ');
			html.push('  </div>');
			html.push('  <div id="kbjzds"></div>');
			html.push('  <div class="mui-input-row mui-input-row-in-view">');
			html.push('    <label style="width:'+this.labelWidth+'">审核材料</label>');
			html.push('    <div id="file_box"></div>');
			html.push('  </div>');
			
			html.push('  <div style="text-align:center;"><button type="button" class="btn btn-primary mui-btn-block" id="'+ulId+'_save_btn">保存</button></div>');
			
			html.push('</form>');
			$("#"+ulId).append(html.join(''));
			SFICheck.iCheck("input[name='shjg']");
			var fileinput = new SFWapFileInput({
				id:"file_box",
				inputId:"pathFile",
				maxFileCount:8
			});
			$(".mui-input-group textarea").attr("placeholder", "请填写");
			if(jutil.isNotEmpty(this.sqid) && jutil.isNotEmpty(this.lxdm)){
				//处理可编辑字段
				var labelWidth = this.labelWidth;
				$.get("content/audit/audit/editfield", "sqid="+this.sqid+"&lxdm="+this.lxdm, function(data){
	  				for(var i in data){
	  					var html = new Array();
	  					html.push('<div class="mui-input-row mui-input-row-in-view"><label style="width:'+labelWidth+'">'+data[i].zdmc+'</label>');
	  					var value = data[i].value == null ? "" : data[i].value;
	  					if("1" == data[i].wjgl){
	  						html.push('<input class="hidden" type="text" id="kbjzd-'+data[i].zddm+'" name="kbjzd-'+data[i].zddm+'" />');
	  						html.push('<input class="form-control" type="text" id="sel-'+data[i].zddm+'" placeholder="请选择"/>');
	  					} else {
	  						html.push('<input class="form-control" id="kbjzd-'+data[i].zddm+'" name="kbjzd-'+data[i].zddm+'" value="'+value+'" placeholder="请填写" />');
	  					}
	  					html.push('</div>');
	  					$("#kbjzds").append(html.join(""));
	  					if("1" == data[i].wjgl){
	  						SFWapSelect.dict("sel-"+data[i].zddm, "kbjzd-"+data[i].zddm, data[i].wjb, value, {
	  							hasEmpty:false
	  						});
	  					}
	  				}
	  			});
			}
			
			var that = this;
			$("#" + ulId + "_save_btn").on("click", function(){
				var url = "";
				var shyj = $("#shyj").val();
				
		    	if(SFICheck.isChecked("shjg1")){//通过
					url="content/audit/audit/auditPass";
				}else if(SFICheck.isChecked("shjg2")){//不通过
					url="content/audit/audit/auditUnPass";
				}else {//退回
					url="content/audit/audit/auditDoBack";
				}
				if(!SFICheck.isChecked("shjg1")){
					if(jutil.isEmpty(shyj)){
		      			 SFAlert.alert("请填写审核意见!");
		      			 return false;
		      		}
				}
				$("#dealWithForm").ajaxSubmit({
				    url : url,
		            type : "POST",
		            async: false,
		            success : function(msg){
		                if(msg.result){
							if(that.auditBackUrl != null && that.auditBackUrl != ""){
								SFAlert.opSuccess({
			      	  				confirm : function(){
			      	            		jutil.redirectToUrl(that.auditBackUrl);
			      	              	}
			      	  			});
							} else {
								SFAlert.opSuccess();
		                   	    that.init(true);
							}
		                }else{
		                    SFAlert.alertError(msg);
		                }
		            }
				});
			});
    	}
    }
    
    /**
     * 获取审批流程的详细申请信息的url
     */
    SFWapView.prototype.setDetailUrl = function(url){
    	this.detailUrl = url;
    }
    /**
     * 审批流程的申请表ID
     */
    SFWapView.prototype.setSqid = function(sqid){
    	this.sqid = sqid;
    }
    /**
     * 审批流程的申请表ID
     */
    SFWapView.prototype.setLxdm = function(lxdm){
    	this.lxdm = lxdm;
    }
    /**
     * 当前审批流程的状态
     */
    SFWapView.prototype.setShzt = function(shzt){
    	this.shzt = shzt;
    }
    
    if (!window.SFWapView) {
        window.SFWapView = SFWapView;
    }
})(jQuery);