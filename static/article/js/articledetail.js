$(document).ready(function () {
    $('.copybtn').each(function () {
        const ButtonId = $(this).attr('id');
        const clipboard = new Clipboard(this);
        clipboard.on('success', function (e) {
            e.clearSelection();
            Swal.fire({
                icon: 'success',
                toast: true,
                position: 'top',
                showConfirmButton: false,
                timer: 3000,
                title: '复制成功',
                width: '150px',
            })
        });
        clipboard.on('error', function (e) {
            console.log('复制失败');
        });
    });
});

$(document).ready(function () {
    $('.delete').on('click', function (event) {
        event.preventDefault();
        const deleteUrl = $(this).attr('href');
        Swal.fire({
            type: 'warning', // 弹框类型
            title: '删除文章', //标题
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

$(document).ready(function () {
    // 当页面滚动时检查是否显示返回顶部按钮
    $(window).scroll(function () {
        if ($(this).scrollTop() > $(window).height()) {
            $('#backToTopBtn').addClass('show');
        } else {
            $('#backToTopBtn').removeClass('show');
        }
    });
    // 当用户点击返回顶部按钮时，页面滚动到顶部
    $('#backToTopBtn').click(function () {
        $('html, body').animate({scrollTop: 0}, 800);
    });
});

$(document).ready(function () {
    $('div.detail-area p img').addClass('thumbnail');

    let currentIndex = 0;
    let rotation = 0;
    const images = $('.thumbnail');
    const modal = $('#modal');
    const modalImg = $('#modal-img');
    const close = $('.close');

    function openModal(index) {
        modal.show();
        currentIndex = index;
        rotation = 0;
        updateImage();
        freezeWindow();
    }

    function closeModal() {
        modal.hide();
        unfreezeWindow();
    }

    function updateImage() {
        modalImg.attr('src', images.eq(currentIndex).attr('src'));
        modalImg.css('transform', `rotate(${rotation}deg)`);
    }

    function showImage(index) {
        if (index < 0 || index >= images.length) {
            closeModal();
        } else {
            currentIndex = index;
            rotation = 0;
            updateImage();
        }
    }

    $('.prev').click(function () {
        showImage(currentIndex - 1);
    });

    $('.next').click(function () {
        showImage(currentIndex + 1);
    });

    $('.rotate').click(function () {
        rotation = (rotation + 90) % 360;
        updateImage();
    });

    images.each(function (index) {
        $(this).click(function () {
            openModal(index);
        });
    });

    close.click(closeModal);

    function freezeWindow() {
        $('body').css('overflow', 'hidden');
    }

    function unfreezeWindow() {
        $('body').css('overflow', 'auto');
    }

    $(window).click(function (event) {
        if ($(event.target).is(modal)) {
            closeModal();
        }
    });
});