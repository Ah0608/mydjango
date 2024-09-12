function swalAlter(icon, title, width = '150px') {
    return Swal.fire({
        icon: icon,
        toast: true,
        position: 'top',
        showConfirmButton: false,
        timer: 3000,
        title: title,
        width: width,
    })
}


$(document).ready(function () {
    $('#date-input').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss'
    });

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
                    swalAlter('success', '创建成功').then(function () {
                        location.reload();
                    });
                },
                error: function () {
                    swalAlter('error', '创建失败')
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
                    swalAlter('success', '修改成功').then(function () {
                        location.reload();
                    });
                },
                error: function () {
                    swalAlter('error', '修改失败')
                }
            });
        }
    });

    $('.start-btn').click(function () {
        const task_id = $(this).data('id');
        let IdArray = []
        IdArray.push(task_id)
        $.ajax({
            url: '/dispatchplatform/start/',
            type: 'POST',
            data: {
                ids: JSON.stringify(IdArray)
            },
            success: function (response) {
                swalAlter('success', '启动成功').then(function () {
                    location.reload();
                });
            },
            error: function () {
                swalAlter('error', '启动失败');
            }
        });
    });

    $('.pause-btn').click(function () {
        const task_id = $(this).data('id');
        let IdArray = []
        IdArray.push(task_id)
        $.ajax({
            url: '/dispatchplatform/pause/',
            type: 'POST',
            data: {
                ids: JSON.stringify(IdArray)
            },
            success: function (response) {
                swalAlter('success', '暂停成功').then(function () {
                    location.reload();
                });
            },
            error: function () {
                swalAlter('error', '暂停失败');
            }
        });
    });

    $('.resume-btn').click(function () {
        const task_id = $(this).data('id');
        let IdArray = []
        IdArray.push(task_id)
        $.ajax({
            url: '/dispatchplatform/resume/',
            type: 'POST',
            data: {
                ids: JSON.stringify(IdArray)
            },
            success: function (response) {
                swalAlter('success', '恢复成功').then(function () {
                    location.reload();
                });
            },
            error: function () {
                swalAlter('error', '恢复失败')
            }
        });
    });

    $('.remove-btn').click(function () {
        const task_id = $(this).data('id');
        let IdArray = []
        IdArray.push(task_id)
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
                    url: '/dispatchplatform/remove/',
                    type: 'POST',
                    data: {
                        ids: JSON.stringify(IdArray),
                    },
                    success: function (response) {
                        swalAlter('success', '删除成功').then(function () {
                            location.reload();
                        });
                    },
                    error: function () {
                        swalAlter('error', '删除失败');
                    }
                });
            } else {
            }
        });
    });

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
                $("#env").val(response.env_variable);
                $("#job_id").val(response.job_id);
            },
            error: function () {
            }
        });
    });
});


$(document).ready(function () {
    $('#inputBox').keypress(function (event) {
        if (event.which === 13) {
            event.preventDefault();
            $('#search-form').submit();
        }
    });

    window.history.replaceState(null, null, '/dispatchplatform/list/');

    $('.view-log').click(function () {
        const job_id = $(this).data('id');
        window.location.href = '/dispatchplatform/viewlog/' + job_id + '/';
    });
});


$(function () {
    const checkAllBox = document.getElementById('checkAll');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');

    checkAllBox.addEventListener('change', function () {
        rowCheckboxes.forEach(function (checkbox) {
            checkbox.checked = checkAllBox.checked;
        });
    });

    rowCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            checkAllBox.checked = Array.from(rowCheckboxes).every(function (cb) {
                return cb.checked;
            });
        });
    });

    function getIdArray() {
        return $('input[class="row-checkbox"]:checked').map(function () {
            return $(this).val();
        }).get()
    }

    $('#pause-tasks').on('click', function () {
        const IdArray = getIdArray()
        if (IdArray.length !== 0) {
            $.ajax({
                url: '/dispatchplatform/pause/',
                type: 'POST',
                data: {
                    ids: JSON.stringify(IdArray)
                },
                success: function (response) {
                    swalAlter('success', '暂停成功').then(function () {
                        location.reload();
                    });
                },
                error: function () {
                    swalAlter('error', '暂停失败')
                }
            });
        } else {
            swalAlter('error', '请选择至少一条数据！', '250px')
        }
    });


    $('#resume-tasks').on('click', function () {
        const IdArray = getIdArray()
        if (IdArray.length !== 0) {
            $.ajax({
                url: '/dispatchplatform/resume/',
                type: 'POST',
                data: {
                    ids: JSON.stringify(IdArray)
                },
                success: function (response) {
                    swalAlter('success', '恢复成功').then(function () {
                        location.reload();
                    });
                },
                error: function () {
                    swalAlter('error', '恢复失败')
                }
            });
        } else {
            swalAlter('error', '请选择至少一条数据！', '250px')
        }
    });

    $('#remove-tasks').on('click', function () {
        const IdArray = getIdArray()
        if (IdArray.length !== 0) {
            Swal.fire({
                type: 'warning',
                title: '删除定时任务',
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
                        url: '/dispatchplatform/remove/',
                        type: 'POST',
                        data: {
                            ids: JSON.stringify(IdArray)
                        },
                        success: function (response) {
                            swalAlter('success', '删除成功').then(function () {
                                location.reload();
                            });
                        },
                        error: function () {
                            swalAlter('error', '删除失败')
                        }
                    });
                } else {
                }
            });
        } else {
            swalAlter('error', '请选择至少一条数据！', '250px')
        }
    });

    $('#start-tasks').on('click', function () {
        const IdArray = getIdArray()
        if (IdArray.length !== 0) {
            $.ajax({
                url: '/dispatchplatform/start/',
                type: 'POST',
                data: {
                    ids: JSON.stringify(IdArray)
                },
                success: function (response) {
                    swalAlter('success', '启动成功').then(function () {
                        location.reload();
                    });
                },
                error: function () {
                    swalAlter('error', '启动失败')
                }
            });
        } else {
            swalAlter('error', '请选择至少一条数据！', '250px')
        }
    });

})