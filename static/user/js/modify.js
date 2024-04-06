// 检查密码是否合法
$(document).ready(function () {
    $('#password').on('input', function () {
        const password = $(this).val();
        const regexDigit = /\d/;
        const regexLetter = /[a-zA-Z]/;
        if (password.length > 0) {
            if (regexDigit.test(password) && regexLetter.test(password)) {
                if (password.length >= 8 && password.length <= 16) {
                    $('#password_feedback').text('密码合法');
                } else {
                    $('#password_feedback').text('密码长度应在8到16之间');
                }
            } else {
                $('#password_feedback').text('密码须同时包含至少一个字母和一个数字');
            }
        } else
            $('#password_feedback').text('');
    });
});

// 检查两次输入的密码是否相同
$(document).ready(function () {
    $('#confirm_pwd').on('input', function () {
        const password = $('#password').val();
        const confirm_pwd = $(this).val();
        if (confirm_pwd.length > 0) {
            if (password !== confirm_pwd) {
                $('#password_error').text('两次输入的密码不一样');
            } else {
                $('#password_error').text('');
            }
        } else {
            $('#password_error').text('');
        }
    });
});
