function loginCheck(){
    if(len = $("#id").val().length == 0){
        
        document.getElementById("msg").innerHTML = "아이디를 입력 해주세요.";
        $("#id").focus();
        return false;
    }
    if(len = $("#pwd").val().length == 0){
        document.getElementById("msg").innerHTML = "비밀번호를 입력 해주세요.";
        $("#pwd").focus();
        return false;
    }

    return true;
}

function signIn(){
    location.href = '/login/signIn/';
}