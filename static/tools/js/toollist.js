$(document).ready(function () {
    $('.box').click(function (event) {
        // 检查点击的目标是否是 <a> 标签
        if ($(event.target).is('a')) {
            return; // 如果是 <a> 标签，直接返回，不执行后面的代码
        }
        window.open($(this).data('url'), '_blank');
    });
});