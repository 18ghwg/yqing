// 立即打卡
function user_dk(){
    $('#user_dk').on('click', function(event){  // user 打卡方法
        var l = Ladda.create(this);
        l.start();
        //定时关闭
        window.setTimeout(function(){
            $(".alert-info").removeClass("show");
        },4000);//显示的时间
        $.ajax({
            url: './dk',
            method: 'POST',
            success: function(res){
                //信息框
                $(".alert-info").addClass("show");
                //对html传值
                document.getElementById("name").innerHTML=res['msg'];
            },
            error: function(msg){
                //信息框
                $(".alert-info").addClass("show");
                var code = msg.status;
                if(code === 429){
                    document.getElementById("name").innerHTML="频繁请求！";
                }else if(code === 500){
                    document.getElementById("name").innerHTML="erro: 接口请求失败！";
                }else if(code === 403){
                    document.getElementById("name").innerHTML="erro: 非法请求！";
                }
            }

        })
        l.stop();
    });
}

// 反馈
function send_fk(){
    $('#send_fk').on('click', function(event){
        //定时关闭
        window.setTimeout(function(){
            $(".alert-info").removeClass("show");
        },3000);//显示的时间
        // 获取参数
        var sbuject = $("input[name='fk_subject']").val();  //主题
        var content = $("textarea[name='fk_content']").val();  //反馈内容
        if(!sbuject){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="主题不能为空！";
            return;
        }
        if(!content){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="反馈内容不能为空";
            return;
        }
        $.ajax({
            url: './fk',
            method: 'POST',
            data: {"subject": sbuject, "content": content},
            success: function(res){
                //信息框
                $(".alert-info").addClass("show");
                //对html传值
                document.getElementById("name").innerHTML=res['msg'];
            },
            error: function(msg){
                //信息框
                $(".alert-info").addClass("show");
                var code = msg.status;
                if(code === 429){
                    document.getElementById("name").innerHTML="频繁请求！";
                }else if(code === 500){
                    document.getElementById("name").innerHTML="erro: 接口请求失败！";
                }else if(code === 403){
                    document.getElementById("name").innerHTML="erro: 非法请求！";
                }
            }

        })
    });
}

// 删除账号
function del_user(){
    $('#del_user').on('click', function(event){
        //定时关闭
        window.setTimeout(function(){
            $(".alert-info").removeClass("show");
        },10000);//显示的时间
        // 获取参数
        var content = $("textarea[name='del_content']").val();  //删除原因
        if(!content){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="删除原因不能为空！";
            return;
        }
        $.ajax({
            url: './del',
            method: 'POST',
            data: {"content": content},
            success: function(res){
                //信息框
                $(".alert-info").addClass("show");
                //对html传值
                document.getElementById("name").innerHTML=res['msg'];
                if(res['code'] === 200){
                    // 跳转到主页
                    setTimeout(function(){
                        window.location.href='./info';
                    },3000);
                }
            },
            error: function(msg){
                //信息框
                $(".alert-info").addClass("show");
                var code = msg.status;
                if(code === 429){
                    document.getElementById("name").innerHTML="频繁请求！";
                }else if(code === 500){
                    document.getElementById("name").innerHTML="erro: 接口请求失败！";
                }else if(code === 403){
                    document.getElementById("name").innerHTML="erro: 非法请求！";
                }
            }

        })
    });
}


// 用户签到
function user_check(){
    $('#check_button').on('click', function(event){
        var check_button=document.getElementById("check_button");  // 获取按钮
        //定时关闭
        window.setTimeout(function(){
            $(".alert-info").removeClass("show");
        },4000);//显示的时间
        $.ajax({
            url: './check',
            method: 'POST',
            success: function(res){
                //信息框
                $(".alert-info").addClass("show");
                //对html传值
                document.getElementById("name").innerHTML=res['msg'];
                if(res.code === 200){
                    check_button.className="btn btn-success btn-sm ladda-button glyphicon glyphicon-ok";  // 隐藏按钮
                    check_button.innerHTML="今日已签到";
                }
            },
            error: function(msg){
                //信息框
                $(".alert-info").addClass("show");
                var code = msg.status;
                if(code === 429){
                    document.getElementById("name").innerHTML="频繁请求！";
                }else if(code === 500){
                    document.getElementById("name").innerHTML="erro: 接口请求失败！";
                }else if(code === 403){
                    document.getElementById("name").innerHTML="erro: 非法请求！";
                }
            }

        })
    });
}

// 兑换卡密
function use_kami(){
    $('#use_kami').on('click', function(event){
        //定时关闭
        window.setTimeout(function(){
            $(".alert-info").removeClass("show");
        },10000);//显示的时间
        // 获取参数
        var kami = $("textarea[name='kami']").val();
        if(!kami){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="卡密不能为空！";
            return;
        }
        $.ajax({
            url: '/user/use/kami',
            method: 'POST',
            data: {"kami": kami},
            success: function(res){
                //信息框
                $(".alert-info").addClass("show");
                //对html传值
                document.getElementById("name").innerHTML=res['msg'];
            },
            error: function(msg){
                //信息框
                $(".alert-info").addClass("show");
                var code = msg.status;
                if(code === 429){
                    document.getElementById("name").innerHTML="频繁请求！";
                }else if(code === 500){
                    document.getElementById("name").innerHTML="erro: 接口请求失败！";
                }else if(code === 403){
                    document.getElementById("name").innerHTML="erro: 非法请求！";
                }
            }

        })
    });
}

// 积分转移
function credit_move(){
    $('#credit_move_button').on('click', function(event){
        //定时关闭
        window.setTimeout(function(){
            $(".alert-info").removeClass("show");
        },10000);//显示的时间
        // 获取参数
        const move_xuehao = document.getElementById("credit_move_xuehao").value;
        const move_num = document.getElementById("credit_move_num").value;
        if(!move_xuehao){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="转移给的学号不能为空！";
            return;
        }if(!move_num){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="转移的积分数不能为空！";
            return;
        }
        $.ajax({
            url: '/user/credit/move',
            method: 'POST',
            data: {"move_xuehao": move_xuehao, "move_num": move_num},
            success: function(res){
                //信息框
                $(".alert-info").addClass("show");
                //对html传值
                document.getElementById("name").innerHTML=res['msg'];
            },
            error: function(msg){
                //信息框
                $(".alert-info").addClass("show");
                var code = msg.status;
                if(code === 429){
                    document.getElementById("name").innerHTML="频繁请求！";
                }else if(code === 500){
                    document.getElementById("name").innerHTML="erro: 接口请求失败！";
                }else if(code === 403){
                    document.getElementById("name").innerHTML="erro: 非法请求！";
                }
            }

        })
    });
}

// 请假额度转移
function quota_move(){
    $('#quota_move_button').on('click', function(event){
        //定时关闭
        window.setTimeout(function(){
            $(".alert-info").removeClass("show");
        },10000);//显示的时间
        // 获取参数
        const move_xuehao = document.getElementById("quota_move_xuehao").value;
        const move_num = document.getElementById("quota_move_num").value;
        if(!move_xuehao){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="转移给的学号不能为空！";
            return;
        }if(!move_num){
            //信息框
            $(".alert-info").addClass("show");
            document.getElementById("name").innerHTML="转移的积分数不能为空！";
            return;
        }
        $.ajax({
            url: '/user/quota/move',
            method: 'POST',
            data: {"move_xuehao": move_xuehao, "move_num": move_num},
            success: function(res){
                //信息框
                $(".alert-info").addClass("show");
                //对html传值
                document.getElementById("name").innerHTML=res['msg'];
            },
            error: function(msg){
                //信息框
                $(".alert-info").addClass("show");
                var code = msg.status;
                if(code === 429){
                    document.getElementById("name").innerHTML="频繁请求！";
                }else if(code === 500){
                    document.getElementById("name").innerHTML="erro: 接口请求失败！";
                }else if(code === 403){
                    document.getElementById("name").innerHTML="erro: 非法请求！";
                }
            }

        })
    });
}


//等待网页加载完成后执行
$(function () {
    user_dk();
    send_fk();
    del_user();
    user_check();
    use_kami();
    credit_move();
    quota_move();
})