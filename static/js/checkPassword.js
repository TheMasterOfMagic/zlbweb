function check(form) {

    // var re = new RegExp
    // {
    //     "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
    // }
    // ;

    // 确认密码栏和重复输入栏不为空
    if (form.password.value == "") {
        alert("密码不能为空!");
        form.password.focus();
        return false;
    }
    elif(form.confirmpassword.value == "")
    {
        alert("请再次输入密码!");
        form.confirmpassword.focus();
        return false;
    }

    //确认两次输入的密码相同
    if (form.password.value != form.confirmpassword.value) {
        alert("两次输入的密码必须相同");
        form.confirmpassword.focus();
        return false;
    }

    if (length(form.password.value) < 8 || length(form.password.value) > 32) {
        alert("密码长度限制在8位~32位");
        form.password.focus();
        return false;
    }

    // if (re.exec(password) == null) {
    //     alert("密码必须同时包含大写小写数字");
    //     form.password.focus();
    //     return false;
    // }

    return true;
}