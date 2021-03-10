function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
    // r[1] if r else undefined
}

// 保存图片验证码编号
var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    // 形成图片验证码的后端地址， 设置到页面中，让浏览请求验证码图片
    // 1. 生成图片验证码编号
    imageCodeId = generateUUID();
    // 设置图片url
    var url = "/api/v1.0/image_codes/" + imageCodeId;
    $(".image-code img").attr("src", url);
}

function sendSMSCode() {
    // 点击发送短信验证码后被执行的函数
    $(".phonecode-a").removeAttr("onclick");    // 移除onclick点击事件
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");    // 增加onclick点击事件，以及事件执行函数
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {

        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    // ajax后台请求数据

    var reg_data = {
        image_code:imageCode,   // 图片验证码的值
        image_code_id:imageCodeId   // 图片验证码的编号，（全局变量）
    };
    $.get("/api/v1.0/sms_codes/"+mobile, reg_data, function(resp){
        if(resp.errno == "0"){
            // 表示发送成功
            var num = 60;
            var timer = setInterval(function () {
                // 修改倒计时文本
                if (num>1){
                    $(".phonecode-a").html(num+"秒");

                }else{
                    $(".phonecode-a").html("获取验证码");
                    $(".phonecode-a").attr("onclick", "sendSMSCode()");
                    // 销毁定时器
                    clearInterval(timer);
                }
                num -= 1;

            }, 1000, 60)
        }else{
            alert(resp.errmsg);
            $(".phonecode-a").attr("onclick", "sendSMSCode()")
        }
    });
    // $(".phonecode-a").attr("onclick", "sendSMSCode()");
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });


    // 为表单的提交添加自定义的函数行为  (行为描述信息，提交事件参数e)
    $(".form-register").submit(function(e){
        // 阻止浏览器对于表单的默认自动提交行为
        e.preventDefault();
        var mobile = $("#mobile").val();
        var phoneCode = $("#phonecode").val();
        var passwd = $("#password").val();
        var passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }

        // 调用ajax向后端发送注册请求
        var req_data = {
            mobile:mobile,
            sms_code:phoneCode,
            passwd:passwd,
            passwd2:passwd2
        };

        var req_json = JSON.stringify(req_data);
        $.ajax({
            url:"/api/v1.0/users",
            type:'post',
            data:req_json,
            contentType: "application/json",
            dataType:'json',
            headers:{
              "X-CSRFToken":getCookie('csrf_token')
            },
            success:function(resp){
                if (resp.errno == "0"){
                    //注册成功，跳转主页
                    location.href = '/index.html';
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    });
});
