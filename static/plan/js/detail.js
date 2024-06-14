/*input 时间输入选择*/
$(".form_datetime").datetimepicker({
    language: 'zh',
    //minView: 'month',
    weekStart: 1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight: 1,
    startView: 2,
    forceParse: 0,
    //format: 'yyyy-mm-dd'
}).on('changeDate', function (ev) {
    $(this).datetimepicker('hide');
});

// select2
$(function () {
    //Initialize Select2 Elements
    $(".select2").select2();
});

$(document).ready(function () {
    $('#btnDelete').on('click', function (event) {
        event.preventDefault();
        const deleteUrl = $(this).attr('href');
        Swal.fire({
            type: 'warning', // 弹框类型
            title: '删除计划', //标题
            text: "删除后将无法恢复，请谨慎操作！", //显示内容
            confirmButtonColor: '#3085d6',// 确定按钮的 颜色
            confirmButtonText: '确定',// 确定按钮的 文字
            showCancelButton: true, // 是否显示取消按钮
            cancelButtonColor: '#d33', // 取消按钮的 颜色
            cancelButtonText: "取消", // 取消按钮的 文字
            focusCancel: true, // 是否聚焦 取消按钮
            reverseButtons: false  // 是否 反转 两个按钮的位置 默认是  左边 确定  右边 取消
        }).then((isConfirm) => {
            //判断 是否 点击的 确定按钮
            if (isConfirm.value) {
                window.location.href = deleteUrl;
            } else {
            }
        });
    });
});