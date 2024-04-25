// 禁止开始检测按钮
$("#start-check").prop("disabled", true);

$(document).ready(function () {
    $("#start-check").click(function () {
        $(".container").append("<div class=\"message\">检测中</div>\n" +
            "<div class=\"spinner\"></div>");
    });
});

// 检测url是否合法
$(document).ready(function () {
    $('#check').on('input', function () {
        const url = $(this).val();
        console.log(url)
        const urlPattern = /^(ftp|http|https):\/\/[^ "]+$/;
        if (urlPattern.test(url)) {
            $("#start-check").prop("disabled", false);
        } else {
            $("#start-check").prop("disabled", true);
        }
    });
});

$(document).ready(function () {
    $(".check-form").submit(function (event) {
        event.preventDefault();
        $("#start-check").prop("disabled", true);
        const formData = $(this).serialize();
        $.post($(this).attr("action"), formData)
            .done(function (response) {
                $("#start-check").prop("disabled", false);
                $(".message").remove();
                $(".spinner").remove();
                console.log("成功");
                window.location.href = "/proxypool/proxylist/";
            })
    });
});

$(document).ready(function () {
    $(".btn-info").click(function () {
        const buttonId = $(this).attr('id');
        console.log(buttonId);
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