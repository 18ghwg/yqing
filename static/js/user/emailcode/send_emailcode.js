
function bindCaptchaBthClick(){
    $('#biaoqian, #xxsend').on('click', function(event){
        //定时关闭
        window.setTimeout(function(){
            $(".alert-info").removeClass("show");
        },3000);//显示的时间
        $.ajax({
            url: '../emailcode/send',
            method: 'POST',
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
    });
}


//等待网页加载完成后执行
$(function () {
    bindCaptchaBthClick()
})