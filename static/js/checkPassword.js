// 检测用户输入的信息是否符合要求，若符合则发送给后端
function beforeSubmit() {

    var username = document.getElementById('userName').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var confirmpassword = document.getElementById('confirmpassword').value;

    var reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/; 

    if(username == ""){
        alert("用户名不能为空");
        return false;
    }
    if(email == ""){
        alert("邮箱不能为空");
        return false;
    }
    if(password == ""){
        alert("密码不能为空");
        return false;
    }
    if(confirmpassword == ""){
        alert("请再次输入密码");
        return false;
    }
    //确认两次输入的密码相同
    if (password != confirmpassword) {
        alert("两次输入的密码必须相同");
        return false;
    }


    if (password.length < 8 || password.length > 32) {
        alert("密码长度限制在8位~32位");
        return false;
    }

    if ((password).match(reg) == null) {
        alert("密码必须同时包含大写小写数字");
        return false;
    }

    // 创建一个FormData对象，直接把表单传进去  
    var formData = new FormData(document.forms.namedItem("login_form"));
        
    // 通过jquery发送出去
    $.ajax({
        url: "/signin",
        type: "POST",
        data: formData,
        processData: false,  // 告诉jQuery不要去处理发送的数据
        contentType: false,   // 告诉jQuery不要去设置Content-Type请求头
        success:function (data) {           //成功回调
            document.open();
            document.write(data);  //根据python返回的模板更新当前页面
            document.close();
        }
    }).done(function(resp) {
        alert('success!');
    }).fail(function(err) {
        alert('fail!')
    });


    return true;

}

//将password使用sha512后发送给后端
function hashPassword(){
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    if(email == ""){
        alert("邮箱不能为空");
        return false;
    }
    if(password == ""){
        alert("密码不能为空");
        return false;
    }

    var formData = new FormData(document.forms.namedItem("login_form"));
    
    // sha512加密过程
    var hash = sha512.create();
    hash.update(password);
    afterhash = hash.hex();

    //表单中password的值用hash值代替
    formData.set('password',afterhash);

    // 通过jquery发送出去
    $.ajax({
        url: "/signup",
        type: "POST",
        data: formData,
        processData: false,  // 告诉jQuery不要去处理发送的数据
        contentType: false,   // 告诉jQuery不要去设置Content-Type请求头
        success:function (data) {           //成功回调
            document.open();
            document.write(data);  //根据python返回的模板更新当前页面
            document.close();
        }
    }).done(function(resp) {
        alert('success!');
    }).fail(function(err) {
        alert('fail!')
    });


    return true;
}