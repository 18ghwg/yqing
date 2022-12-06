// 后台查电费
function user_login(){
    $('#user_login').on('click', function(event){
        var xuehao = $("input[name='xuehao']").val();
        var password = jiami($("input[name='password']").val());
        $.ajax({
            url: '/user/login',
            method: 'POST',
            data: {"xuehao": xuehao, "password": password},
            success: function(res){
                if(res.code === 200){
                    console.log(res.msg);
                }else{
                    console.log(res.msg);
                }
            },
            error: function(msg){
                //信息框
                $(".alert-info").addClass("show");
                var code = msg.status;
                if(code === 429){
                    document.getElementById("room_power").innerHTML="频繁请求！";
                }else if(code === 500){
                    document.getElementById("room_power").innerHTML="erro: 接口请求失败！";
                }else if(code === 403){
                    document.getElementById("room_power").innerHTML="erro: 非法请求！";
                }
            }

        })
    })
}


//等待网页加载完成后执行
$(function () {
    user_login();
})


