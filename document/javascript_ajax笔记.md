```
$(".phonecode-a").removeAttr("onclick");
var mobile = $("#mobile").val();

id="mobile"	>> #mobile
```

```
ajax后台请求数据
如何判断ajax使用简写的还是完整形式的，如果只是请求的话使用简写形似，如果需要修改headers头部信息或者其他的信息则用完整形式．
```



ajax请求形式

```
var reg_data = {
	image_code:imageCode,
	image_code_id:imageCodeId
}
$.get("/api/v1.0/sms_codes/"+mobile, reg_data, function(data){})
```

```
$.get("/api/v1.0/sms_codes/"+mobile+"?image_code=xxxxximage_code_id=xxxx", function(data){})
```

```
// ajax后台请求数据

var reg_data = {
    image_code:imageCode,   // 图片验证码的值
    image_code_id:imageCodeId   // 图片验证码的编号，（全局变量）
};
$.get("/api/v1.0/sms_codes/"+mobile, reg_data,
	function(data){

}, 'json'); 
```

18320261704