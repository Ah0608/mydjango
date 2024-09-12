// 禁止开始检测按钮
$("#start-check").prop("disabled", true);

// 检测url是否合法
$(document).ready(function () {
    $('#check').on('input', function () {
        const url = $(this).val();
        const urlPattern = /^(ftp|http|https):\/\/[^ "]+$/;
        if (urlPattern.test(url)) {
            $("#start-check").prop("disabled", false);
        } else {
            $("#start-check").prop("disabled", true);
        }
    });
});


$(document).ready(function () {
    $("#start-check").click(function () {
        const url = $("#check").val()
        $("#start-check").prop("disabled", true);
        Swal.fire({
            title: '代理检测',
            text: '代理正在检查中，请稍等...',
            icon: 'warning',
            showConfirmButton: false,
        });
        $.ajax({
            type: "POST",
            url: '/proxypool/checkproxy/',
            data: {'url': url},
            success: function (response) {
                // $("#start-check").prop("disabled", false);
                // $(".message").remove();
                // $(".spinner").remove();
                window.location.reload();
            },
            error: function () {
                $("#check").val("");
                Swal.fire({
                    icon: 'error',
                    toast: true,
                    position: 'top',
                    showConfirmButton: false,
                    timer: 3000,
                    title: '检测失败',
                    width: '150px',
                })
            }
        });
    });
});

$(document).ready(function () {
    $(".btn-info").click(function () {
        const buttonId = $(this).attr('id');
        const ip = $(this).closest("tr").find("td:first").text();
        const ipType = $(this).closest("tr").find("td:nth-child(2)").text();
        const textToCopy = ipType + "://" + ip

        const tempInput = $("<input>");
        $("body").append(tempInput);
        tempInput.val(textToCopy).select();
        document.execCommand("copy");
        tempInput.remove();
        $("#" + buttonId).text('已复制')
        setTimeout(function () {
            $("#" + buttonId).text('复制IP');
        }, 3000);
    });
});

$(document).ready(function () {
    $('.del-btn').click(function () {
        const del_id = $(this).data('id');
        Swal.fire({
            type: 'warning',
            title: '删除该IP！',
            text: "删除后将无法恢复，请谨慎操作！",
            confirmButtonColor: '#3085d6',
            confirmButtonText: '确定',
            showCancelButton: true,
            cancelButtonColor: '#d33',
            cancelButtonText: "取消",
            focusCancel: true,
            reverseButtons: false
        }).then((isConfirm) => {
            if (isConfirm.value) {
                $.ajax({
                    url: '/proxypool/deleteproxy/',
                    type: 'POST',
                    data: {'del_id': del_id},
                    success: function (response) {
                        Swal.fire({
                            icon: 'success',
                            toast: true,
                            position: 'top',
                            showConfirmButton: false,
                            timer: 3000,
                            title: 'IP删除成功',
                            width: '150px',
                        })
                        window.location.reload();
                    },
                    error: function () {
                        Swal.fire({
                            icon: 'error',
                            toast: true,
                            position: 'top',
                            showConfirmButton: false,
                            timer: 3000,
                            title: 'IP删除失败',
                            width: '150px',
                        })
                    }
                });
            }
        })
    });
});

