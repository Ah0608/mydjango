$(function () {
    $('#date-input').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss'
    });
});


$(document).ready(function () {
    $('#select-field').change(function () {
        const selectedOption = $(this).val();
        if (selectedOption === "date") {
            const newContent1 = `
            <div class='input-group date' id='date-input'>
                <input type='text' class="form-control">
                <span class="input-group-addon">
                <span class="glyphicon glyphicon-calendar"></span>
            </span>
            </div>
            `;
            $('.time-container').empty().append(newContent1); // 添加新内容
        } else if (selectedOption === "interval") {
            console.log('interval')
            const newContent2 = `
            <div class="input-group" id="interval-input">
                <input type="number" name="num" class="form-control" id="interval" min="1">
                <span class="input-group-addon">Every</span>
                <select class="form-control" name="unit" id="unit">
                    <option value="days">天</option>
                    <option value="hours">小时</option>
                    <option value="minutes">分钟</option>
                    <option value="seconds">秒</option>
                </select>
            </div>
            `;
            $('.time-container').empty().append(newContent2);
        } else if (selectedOption === "cron") {
            const newContent3 = `
            <div class="input-group cron" id="cron-input">
                <input type="text" name="timeexp" class="form-control" placeholder="定时表达式" required="">
            </div>
            `;
            $('.time-container').empty().append(newContent3);
        }
    });
});


$(document).ready(function () {
    $('#task-btn').click(function (event) {
        const classValue = $(this).attr('class');
        if (classValue === 'create-button') {
            const formData = $('.task-form').serialize();
            $.ajax({
                url: '/dispatchplatform/create/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    $("#PlatFormModal").modal('hide');
                    Swal.fire({
                        icon: 'success',
                        toast: true,
                        position: 'top',
                        showConfirmButton: false,
                        timer: 3000,
                        title: '创建成功',
                        width: '150px',
                    }).then(function () {
                        location.reload();
                    });
                },
                error: function () {
                    Swal.fire({
                        icon: 'error',
                        toast: true,
                        position: 'top',
                        showConfirmButton: false,
                        timer: 3000,
                        title: '创建失败',
                        width: '150px',
                    })
                }
            });
        } else {
            const formData = $('.task-form').serialize();
            $.ajax({
                url: '/dispatchplatform/modify/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    $("#ModifyModal").modal('hide');
                    Swal.fire({
                        icon: 'success',
                        toast: true,
                        position: 'top',
                        showConfirmButton: false,
                        timer: 3000,
                        title: '修改成功',
                        width: '150px',
                    }).then(function () {
                        location.reload();
                    });
                },
                error: function () {
                    Swal.fire({
                        icon: 'error',
                        toast: true,
                        position: 'top',
                        showConfirmButton: false,
                        timer: 3000,
                        title: '修改失败',
                        width: '150px',
                    })
                }
            });
        }
    });
});

$(document).ready(function () {
    $('.start-btn').click(function () {
        const pk = $(this).data('id');
        $.ajax({
            url: '/dispatchplatform/start/' + pk + '/',
            type: 'POST',
            data: {},
            success: function (response) {
                Swal.fire({
                    icon: 'success',
                    toast: true,
                    position: 'top',
                    showConfirmButton: false,
                    timer: 3000,
                    title: '启动成功',
                    width: '150px',
                }).then(function () {
                    location.reload();
                });
            },
            error: function () {
                Swal.fire({
                    icon: 'error',
                    toast: true,
                    position: 'top',
                    showConfirmButton: false,
                    timer: 3000,
                    title: '启动失败',
                    width: '150px',
                }).then(function () {
                    location.reload();
                });
            }
        });
    });
});

$(document).ready(function () {
    $('.pause-btn').click(function () {
        const task_id = $(this).data('id');
        $.ajax({
            url: '/dispatchplatform/pause/' + task_id + '/',
            type: 'POST',
            data: {},
            success: function (response) {
                Swal.fire({
                    icon: 'success',
                    toast: true,
                    position: 'top',
                    showConfirmButton: false,
                    timer: 3000,
                    title: '暂停成功',
                    width: '150px',
                }).then(function () {
                    location.reload();
                });
            },
            error: function () {
                Swal.fire({
                    icon: 'error',
                    toast: true,
                    position: 'top',
                    showConfirmButton: false,
                    timer: 3000,
                    title: '暂停失败',
                    width: '150px',
                }).then(function () {
                    location.reload();
                });
            }
        });
    });
});

$(document).ready(function () {
    $('.resume-btn').click(function () {
        const task_id = $(this).data('id');
        $.ajax({
            url: '/dispatchplatform/resume/' + task_id + '/',
            type: 'POST',
            data: {},
            success: function (response) {
                Swal.fire({
                    icon: 'success',
                    toast: true,
                    position: 'top',
                    showConfirmButton: false,
                    timer: 3000,
                    title: '恢复成功',
                    width: '150px',
                }).then(function () {
                    location.reload();
                });
            },
            error: function () {
                Swal.fire({
                    icon: 'error',
                    toast: true,
                    position: 'top',
                    showConfirmButton: false,
                    timer: 3000,
                    title: '恢复失败',
                    width: '150px',
                }).then(function () {
                    location.reload();
                });
            }
        });
    });
});

$(document).ready(function () {
    $('.remove-btn').click(function () {
        const task_id = $(this).data('id');
        Swal.fire({
            type: 'warning', // 弹框类型
            title: '删除定时任务', //标题
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
                $.ajax({
                    url: '/dispatchplatform/remove/' + task_id + '/',
                    type: 'POST',
                    data: {},
                    success: function (response) {
                        Swal.fire({
                            icon: 'success',
                            toast: true,
                            position: 'top',
                            showConfirmButton: false,
                            timer: 3000,
                            title: '删除成功',
                            width: '150px',
                        }).then(function () {
                            location.reload();
                        });
                    },
                    error: function () {
                        Swal.fire({
                            icon: 'error',
                            toast: true,
                            position: 'top',
                            showConfirmButton: false,
                            timer: 3000,
                            title: '删除失败',
                            width: '150px',
                        }).then(function () {
                            location.reload();
                        });
                    }
                });
            } else {
            }
        });
    });
});

$(document).ready(function () {
    $(".modify-btn").click(function () {
        $("#PlatFormModal").modal();
        $("#PlatFormModalLabel").text('修改任务');
        $("#task-btn").text('确定修改');
        $('#task-btn').removeClass('create-button').addClass('modify-button');
        $("#job_id").prop("readonly", true);
        const job_id = $(this).data('id');

        $.ajax({
            url: '/dispatchplatform/modify/',
            type: 'GET',
            data: {'job_id': job_id},
            success: function (response) {
                $("#taskname").val(response.task_name);
                $("#python-path").val(response.python_path);
                $("#taskfile").val(response.task_file);
                $("#job_id").val(response.job_id);
            },
            error: function () {
            }
        });
    });
});


$(document).ready(function () {
    $('#inputBox').keypress(function (event) {
        // 判断按下的键是否是回车键
        if (event.which === 13) {
            event.preventDefault();
            $('#search-form').submit();
        }
    });
});


$(document).ready(function () {
    // 禁用“确认重新提交表单”
    window.history.replaceState(null, null, '/dispatchplatform/list/');
});


$(document).ready(function () {
    $('.view-log').click(function () {
        const job_id = $(this).data('id');
        window.location.href = '/dispatchplatform/viewlog/' + job_id + '/';
    });
});
