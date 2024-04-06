// 禁止获取验证码按钮
$("#sendButton").prop("disabled", true);

// 检查邮箱格式
$(document).ready(function () {
    $('#email').on('input', function () {
        const email = $(this).val();
        if (email.length > 0) {
            const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (emailPattern.test(email)) {
                $('.code-button').css('opacity', '1');
                $("#sendButton").prop("disabled", false);
                $("#email_error").text('')
            } else {
                $("#sendButton").prop("disabled", true);
                $('.code-button').css('opacity', '0.65');
                $("#email_error").text('请输入正确的邮箱')
            }
        } else {
            $("#email_error").text('')
        }
    })
});

// 发送邮箱验证码
function sendEmail() {
    const email = $('#email').val();
    $.ajax({
        url: '/forget/sendmeail/',
        type: 'POST',
        data: {
            'email': email
        },
        success: function (response) {
            if (response.flag) {
                $('#email_error').text(response.message);
                $('.code-button').css('opacity', '0.65');
                $('#sendButton').prop('disabled', true);
                // 倒计时60秒
                var seconds = 60;
                const countdownElement = $('#countdown');
                const countdownInterval = setInterval(function () {
                    seconds--;
                    countdownElement.text(seconds);
                    if (seconds <= 0) {
                        clearInterval(countdownInterval);
                        countdownElement.text('');
                        $('#sendButton').prop('disabled', false); // 启用发送按钮
                    }
                }, 1000);
            } else {
                $('#email_error').text(response.message);
            }
        }
    });
}