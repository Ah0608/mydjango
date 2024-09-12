$(document).ready(function () {
    // 禁用“确认重新提交表单”
    window.history.replaceState(null, null, '/article/list/');
});


$(document).ready(function () {
    $('#add_article').click(function () {
        window.location.href = '/article/create/'
    });
});