function set_info() {
    $('#form_body_save_btn').on('click', function(event){
        let qjlb=document.getElementById("qjlb").value;  //请假类别
        const kssj = $("input[name='kssj']").val();  //开始时间
        const jssj = $("input[name='jssj']").val();  //结束时间
        const bz = $("input[name='bz']").val();  //请假事由

        if (!qjlb){
            SFAlert.alert("请选择请假类别！");
            return;
        }if (!kssj){
            SFAlert.alert("请选择开始时间！");
            return;
        }if (!jssj){
            SFAlert.alert("请选择结束时间！");
            return;
        }if (!bz){
            SFAlert.alert("请填写请假事由！");
            return;
        }
        $.ajax({
            url: '#',
            method: 'POST',
            data: {"qjlb": qjlb, "kssj": kssj, "jssj": jssj, "bz": bz},
            beforeSend: function () {
                layer.msg('提交中...', {
                    anim: 3,
                    icon: 16,
                    time: 4000,
                    offset: '230px',
                    shade: [0.8, '#393D49'],
                });
            },
            success: function(res){
                $('#qjm-info-modal').modal({
                    keyboard: false
                })
                if (res.code === 200){
                    document.getElementById('qjm-info-msg').innerHTML=res.msg+'<br><a href="/qjm/home" class="btn btn-info btn-lg ladda-button" data-style="zoom-in" data-size="l"><span class="glyphicon glyphicon-qrcode">前往工作台</span></a>';
                }
                if (res.code === 400){
                    document.getElementById('qjm-info-msg').innerHTML=res.msg;
                }
            },
            error: function(msg){
                //信息框
                $(".alert-info").addClass("show");
                var code = msg.status;
                if(code === 429){
                    layer.msg('频繁请求', {
                    anim: 3,
                    icon: 16,
                    time: 500,
                    offset: '230px',
                    shade: [0.8, '#393D49'],
                });
                }else if(code === 500){
                    layer.msg('erro：接口请求失败', {
                    anim: 3,
                    icon: 16,
                    time: 500,
                    offset: '230px',
                    shade: [0.8, '#393D49'],
                });
                }else if(code === 403){
                    layer.msg('方法错误', {
                    anim: 3,
                    icon: 16,
                    time: 500,
                    offset: '230px',
                    shade: [0.8, '#393D49'],
                });
                }
            }

        });
    });
}


//等待网页加载完成后执行
$(function () {
    set_info();
})
