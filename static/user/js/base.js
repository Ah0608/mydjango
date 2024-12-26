// function _0x26f2(){const _0x5537b8=['#confirm-pwd','5353439caNIEg','134460DEzlsr','2zHJhry','84JPBmcl','14230ZJWKeV','length','input','text','val','密码须同时包含至少一个字母和一个数字','8HkzMvA','474665GoSHsY','两次输入的密码不一样','76lEtPNW','6ZhXbBx','ready','#password_feedback','9820069rjiudV','relatedTarget','#new-pwd','1353GafeBx','test','show.bs.modal','#password_error','#passwordModal','密码合法','7831285muHUip','#AvatarModal','8889309aSnTbl'];_0x26f2=function(){return _0x5537b8;};return _0x26f2();}function _0x5375(_0x4555e3,_0x3cec19){const _0x26f249=_0x26f2();return _0x5375=function(_0x5375fa,_0x26d22a){_0x5375fa=_0x5375fa-0xd2;let _0x453ec9=_0x26f249[_0x5375fa];return _0x453ec9;},_0x5375(_0x4555e3,_0x3cec19);}const _0x23a823=_0x5375;(function(_0x49b0a5,_0x57c9f2){const _0x5e05b1=_0x5375,_0x116b22=_0x49b0a5();while(!![]){try{const _0x5626fb=parseInt(_0x5e05b1(0xe4))/0x1*(parseInt(_0x5e05b1(0xdb))/0x2)+parseInt(_0x5e05b1(0xda))/0x3*(-parseInt(_0x5e05b1(0xe6))/0x4)+-parseInt(_0x5e05b1(0xd5))/0x5*(-parseInt(_0x5e05b1(0xe7))/0x6)+parseInt(_0x5e05b1(0xea))/0x7+parseInt(_0x5e05b1(0xe3))/0x8*(parseInt(_0x5e05b1(0xd7))/0x9)+-parseInt(_0x5e05b1(0xdd))/0xa*(-parseInt(_0x5e05b1(0xed))/0xb)+parseInt(_0x5e05b1(0xdc))/0xc*(-parseInt(_0x5e05b1(0xd9))/0xd);if(_0x5626fb===_0x57c9f2)break;else _0x116b22['push'](_0x116b22['shift']());}catch(_0x1760a7){_0x116b22['push'](_0x116b22['shift']());}}}(_0x26f2,0xd4f7e),$(_0x23a823(0xd6))['on'](_0x23a823(0xef),function(_0x488b0c){const _0x2b3f63=_0x23a823;$(_0x488b0c[_0x2b3f63(0xeb)]);}),$(_0x23a823(0xd3))['on']('show.bs.modal',function(_0x35088a){const _0x1a555c=_0x23a823;$(_0x35088a[_0x1a555c(0xeb)]);}),$(document)[_0x23a823(0xe8)](function(){const _0x386dc9=_0x23a823;$(_0x386dc9(0xec))['on'](_0x386dc9(0xdf),function(){const _0x11b8d4=_0x386dc9,_0x3a7137=$(this)[_0x11b8d4(0xe1)](),_0x3132c2=/\d/,_0x457722=/[a-zA-Z]/;if(_0x3a7137[_0x11b8d4(0xde)]>0x0)_0x3132c2[_0x11b8d4(0xee)](_0x3a7137)&&_0x457722[_0x11b8d4(0xee)](_0x3a7137)?_0x3a7137[_0x11b8d4(0xde)]>=0x8&&_0x3a7137[_0x11b8d4(0xde)]<=0x10?$(_0x11b8d4(0xe9))[_0x11b8d4(0xe0)](_0x11b8d4(0xd4)):$(_0x11b8d4(0xe9))[_0x11b8d4(0xe0)]('密码长度应在8到16之间'):$('#password_feedback')[_0x11b8d4(0xe0)](_0x11b8d4(0xe2));else $('#password_feedback')[_0x11b8d4(0xe0)]('');});}),$(document)['ready'](function(){const _0x1f7518=_0x23a823;$(_0x1f7518(0xd8))['on'](_0x1f7518(0xdf),function(){const _0x3bfd3d=_0x1f7518,_0x320d09=$(_0x3bfd3d(0xec))['val'](),_0x3894a8=$(this)[_0x3bfd3d(0xe1)]();_0x3894a8['length']>0x0?_0x320d09!==_0x3894a8?$(_0x3bfd3d(0xd2))[_0x3bfd3d(0xe0)](_0x3bfd3d(0xe5)):$(_0x3bfd3d(0xd2))[_0x3bfd3d(0xe0)](''):$(_0x3bfd3d(0xd2))[_0x3bfd3d(0xe0)]('');});}));
$('#AvatarModal').on('show.bs.modal', function (event) {
    $(event.relatedTarget)
})
$('#passwordModal').on('show.bs.modal', function (event) {
    $(event.relatedTarget)
})

// 检查密码是否合法
$(document).ready(function () {
    $('#new-pwd').on('input', function () {
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
    $('#confirm-pwd').on('input', function () {
        const password = $('#new-pwd').val();
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

$(document).ready(function () {

    const hour = new Date().getHours();
    let greeting;
    if (hour >= 5 && hour < 12) {
        greeting = "早上好";
    } else if (hour >= 12 && hour < 18) {
        greeting = "下午好";
    } else {
        greeting = "晚上好";
    }

    // 将问候语显示在页面上
    $(".greeting").text(greeting);

    function updateDateTime() {
        // 获取当前日期和时间
        const now = new Date();
        const year = now.getFullYear();
        const month = now.getMonth() + 1;
        const date = now.getDate();

        const formattedTime = year + '年' + month + '月' + date + '日 '
        $('#currentDateTime').text(formattedTime);
    }

    updateDateTime()
});
