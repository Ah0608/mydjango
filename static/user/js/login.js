$('.captcha').click(function () {
    $.getJSON("/captcha/refresh/", function (result) {
        $('.captcha').attr('src', result['image_url']);
        $('#id_captcha_0').val(result['key'])
    });
});
// 是否显示密码
const passwordInput = document.getElementById('password');
const eyeIcon = document.getElementById('eyes');

eyeIcon.addEventListener('click', function () {
    const type = passwordInput.getAttribute('type')
    console.log(type)
    if (type === 'password') {
        eyeIcon.setAttribute("src", "../static/user/images/open.png")
        passwordInput.setAttribute('type', 'text');
    } else {
        eyeIcon.setAttribute("src", "../static/user/images/close.png")
        passwordInput.setAttribute('type', 'password');
    }
});