$(document).ready(function() {
    $('.copybtn').each(function() {
        const clipboard = new Clipboard(this);
        clipboard.on('success', function(e) {
            console.log('复制成功');
        });
        clipboard.on('error', function(e) {
            console.log('复制失败');
        });
    });
});

$(document).ready(function () {
    $('.delete').on('click', function (event) {
        event.preventDefault();
        const deleteUrl = $(this).attr('href');
        const result = confirm("确定要删除吗？");
        if (result) {
            window.location.href = deleteUrl;
        } else {
        }
    });
});