$(document).ready(function () {
    $('#curlInput').on('input', function () {
        const curlCommand = $('#curlInput').val();
        if (curlCommand === '') {
            $('#pythonOutput').text('')
            $('.code').hide()
            $('#errormessage').hide()
        } else {
            $.ajax({
                url: '/tools/curl/',
                method: 'POST',
                data: {
                    'curl_command': curlCommand,
                },
                success: function (response) {
                    if (response.status) {
                        $('.code').show()
                        $('#pythonOutput').text(response.python_code);
                    } else {
                        $('#errormessage').show().text(response.error_message);
                    }
                },
            });
        }
    });
    $('#copyButton').click(function () {
        const text = $('#pythonOutput').text();
        const displayValue = $('.code').css('display');
        if (displayValue === 'none') {
            Swal.fire({
                icon: 'error',
                toast: true,
                position: 'top',
                showConfirmButton: false,
                timer: 3000,
                title: '没有可复制的内容！',
                width: '250px',
            })
        } else {
            const $temp = $("<textarea>");
            $("body").append($temp);
            $temp.val(text).select();
            document.execCommand("copy");
            $temp.remove();
            Swal.fire({
                icon: 'success',
                toast: true,
                position: 'top',
                showConfirmButton: false,
                timer: 3000,
                title: '内容已复制到剪贴板！',
                width: '250px',
            })
        }
    });
    $('#clearButton').click(function () {
        $('#curlInput').val('')
        $('#pythonOutput').text('')
        $('.code').hide()
        $('#errormessage').hide()
    });
});