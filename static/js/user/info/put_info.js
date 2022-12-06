
function bindCaptchaBthClick(){
    $('#put_info').on('click', function(event){
        //定时关闭
        window.setTimeout(function(){
            $(".alert-info").removeClass("show");
        },6000);//显示的时间
        var email = $("input[name='email']").val();
        var user_state = $("input[name='user_state']").val();
        var dk_time = $("input[name='dk_time']").val();
        var password = $("input[name='password']").val();
        var room_num = $("input[name='room_num']").val();  // 宿舍号
        if(!email){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="邮箱不能为空！";
            return;
        } else if(email.indexOf('@') === -1){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="邮箱格式不正确！";
            return;
        } else if(!password){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="密码不能为空！";
            return;
        } else if(!user_state){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="参数有误！";
            return;
        } else if(!dk_time){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="打卡时间不能为空！";
            return;
        }
        if(user_state !== '5')
        {
            var qqh = $("input[name='qqh']").val();
            if(!qqh){
                //信息框
                $(".alert-info").addClass("show");
                document.getElementById("name").innerHTML="QQ不能为空！";
                return;
            }
            $.ajax({
                url: './put',
                method: 'POST',
                data: {"email": email, "password": password, "qqh": qqh, "user_state": user_state, "dk_time": dk_time, "room_num": room_num},
                beforeSend: function () {
                    layer.msg('保存中...', {
                        anim: 3,
                        icon: 16,
                        time: 1000,
                        offset: '230px',
                        shade: [0.8, '#393D49'],
                    });
                },
                success: function(res){
                    //信息框
                    $(".alert-info").addClass("show");
                    //对html传值
                    document.getElementById("name").innerHTML=res['msg'];
                },
                error: function(data){
                    //信息框
                    $(".alert-info").addClass("show");
                    var code = data.status;  //状态码
                    if(code === 429){
                        document.getElementById("name").innerHTML="频繁请求！";
                    }else if(code === 403){
                        document.getElementById("name").innerHTML="erro: 非法请求！";
                    }

                }

            })
        } else if(user_state === '5') {
            var xuehao = $("input[name='xuehao']").val();
            if(!xuehao){
                //信息框
                $(".alert-info").addClass("show");
                document.getElementById("name").innerHTML="学号不能为空！";
                return;
            }
            $.ajax({
                url: '../add',
                method: 'POST',
                data: {"addemail": email, "addmima": password, "addxuehao": xuehao, "dk_time": dk_time},
                success: function(res){
                    //信息框
                    $(".alert-info").addClass("show");
                    var content;  // 弹窗内容
                    if(res.indexOf("账号信息") !== -1){  //提交成功
                        content = "提交成功！";
                        // 跳转到后台主页
                        setTimeout(function(){
                            window.location.href='';
                        },3000);
                    } else if(res.indexOf("账号密码错误") !== -1){
                        content  = "账号或密码错误！";
                    } else if(res.indexOf("时间有误") !== -1){
                        content = "打卡时间有误！<br>学校网站还没开机呢！";
                    } else if(res.indexOf("超时") !== -1){
                        content = "学校服务器还没开机<br>不能添加！";
                    } else if(res.indexOf("邮箱重复") !== -1){
                        content = "你填写的邮箱已被占用！";
                    } else if(res.indexOf("重复提交") !== -1){
                        content = "你的账号已存在<br>不要再提交了！";
                    } else if(res.indexOf("限制") !== -1){
                        content = "你的账号提交次数过多！";
                    } else if(res.indexOf("黑名单") !== -1){
                        content = "黑名单提交个屁！";
                    } else if(res.indexOf("邮箱不正确") !== -1){
                        content = "邮箱填写格式有误！";
                    } else{
                        content = "提交失败！";
                    }
                    document.getElementById("name").innerHTML=content;
                },
                error: function(data){
                    //信息框
                    $(".alert-info").addClass("show");
                    var code = data.status;  //状态码
                    if(code === 429){
                        document.getElementById("name").innerHTML="频繁请求！";
                    }else if(code === 403){
                        document.getElementById("name").innerHTML="erro: 非法请求！";
                    }else if(code === 500){
                        document.getElementById("name").innerHTML="erro: 接口请求失败！";
                    }

                }

            })
        }

    });
}


//等待网页加载完成后执行
$(function () {
    bindCaptchaBthClick()
})