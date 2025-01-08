$(function () {
    let collapsed = false;
    let json_input = $('#json-input');
    let error_message = $('#error-message');
    let searchIndex = -1;
    let matches = [];

    function renderJson() {
        let inputContent = json_input.val().trim();
        if (inputContent === "") {
            $('#json-renderer').empty();
            error_message.hide();

            matches = [];
            searchIndex = -1;
            updateMatchCount();

            return;
        }
        try {
            inputContent = inputContent.replace(/([,{]\s*)'([^']+)'\s*:/g, '$1"$2":').replace(/:\s*'([^']*)'/g, ': "$1"').replace(/\bNone\b/g, 'null');
            error_message.hide();
            let input = JSON.parse(inputContent);
            const options = {
                collapsed: collapsed
            };
            $('#json-renderer').jsonViewer(input, options);
            matches = [];
            searchIndex = -1;
            highlightMatches();
            updateMatchCount();
        } catch (error) {
            $('#json-renderer').empty();
            error_message.text(error + '/请输入有效的JSON数据')
            error_message.show();
        }
    }

    function highlightMatches() {
        // 清除上一次搜索的高亮效果
        $('#json-renderer .highlight').each(function () {
            const parent = $(this).parent();
            $(this).replaceWith($(this).text());
            parent[0].normalize();
        });

        $('#json-renderer .highlight-navigation').removeClass('highlight-navigation');
        matches = [];

        const searchText = $('#search-box').val().trim();
        if (searchText === '') {
            updateMatchCount();
            return;
        }

        const regex = new RegExp(searchText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');

        // 递归查找包含匹配项的元素，并展开它们的折叠父级
        function findAndHighlightMatches($element) {
            $element.contents().each(function () {
                if (this.nodeType === 3) { // 文本节点
                    const text = this.textContent;
                    let match;
                    let lastIndex = 0;
                    while ((match = regex.exec(text)) !== null) {
                        const matchStart = match.index;
                        const matchEnd = matchStart + match[0].length;
                        const beforeMatch = text.substring(lastIndex, matchStart);
                        const matchText = text.substring(matchStart, matchEnd);

                        // 创建包含高亮的 span 元素
                        const $highlightedSpan = $('<span class="highlight"></span>');
                        $highlightedSpan.text(matchText);

                        // 创建未匹配的文本节点
                        const $beforeText = document.createTextNode(beforeMatch);

                        // 将新的节点添加到 DOM 中
                        $(this).before($beforeText);
                        $(this).before($highlightedSpan);

                        // 更新 lastIndex
                        lastIndex = matchEnd;
                    }

                    // 如果有剩余文本，创建未匹配的文本节点
                    if (lastIndex < text.length) {
                        const remainingText = text.substring(lastIndex);
                        const $remainingText = document.createTextNode(remainingText);
                        $(this).before($remainingText);
                    }

                    // 删除原始文本节点
                    $(this).remove();
                } else if (this.nodeType === 1) { // 元素节点
                    findAndHighlightMatches($(this));
                }
            });
        }

        findAndHighlightMatches($('#json-renderer'));
        matches = $('#json-renderer .highlight');
        updateMatchCount();

        if (matches.length > 0) {
            searchIndex = 0;
            $(matches[searchIndex]).addClass('highlight-navigation');
            $(matches[searchIndex])[0].scrollIntoView({behavior: 'smooth', block: 'center'});
        }
    }


    function navigateMatch(direction) {
        if (matches.length === 0) return;

        $(matches[searchIndex]).removeClass('highlight-navigation');
        searchIndex = (searchIndex + direction + matches.length) % matches.length;
        $(matches[searchIndex]).addClass('highlight-navigation');
        matches[searchIndex].scrollIntoView({behavior: 'smooth', block: 'center'});
        updateMatchCount();
    }

    function updateMatchCount() {
        const current = matches.length > 0 ? searchIndex + 1 : 0;
        const total = matches.length;
        $('#match-count').text(current + ' / ' + total);
    }

    json_input.on('input', renderJson);
    $('#search-box').on('input', highlightMatches);
    $('#next-btn').on('click', function () {
        navigateMatch(1);
    });
    $('#prev-btn').on('click', function () {
        navigateMatch(-1);
    });
    $('#toggle-collapsed-btn').on('click', function () {
        collapsed = !collapsed;
        renderJson();
        $(this).find('i').attr('class', `fas fa-${collapsed ? 'maximize' : 'minimize'}`);
        $(this).find('span').text(collapsed ? ' 展开' : ' 折叠');
    });

    $('#search-box').on('keydown', function (e) {
        if (e.key === 'Enter') {
            $('#next-btn').click();
        }
    });

    renderJson();
});


function getPath(s) {
    const plist = [];
    s.split('.').forEach(i => {
        if (i.includes('[') && i.includes(']')) {
            // 如果包含数组索引部分
            const index = i.indexOf('[');
            const p1 = i.slice(0, index); // 获取属性名
            const p2 = i.slice(index);    // 获取索引部分
            const part = `['${p1}']${p2}`;
            plist.push(part);
        } else {
            // 普通属性名部分
            const part = `['${i}']`;
            plist.push(part);
        }
    });

    return plist.join('');
}

(function ($) {
    function isCollapsable(arg) {
        return arg instanceof Object && Object.keys(arg).length > 0;
    }

    function json2html(json, options, path = '') {
        let html = '';
        if (typeof json === 'string') {
            json = json.replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/'/g, '&apos;')
                .replace(/"/g, '&quot;');
            json = json.replace(/&quot;/g, '\\&quot;');
            html += `<span class="json-string">"${json}"</span>`;
        } else if (typeof json === 'number') {
            html += `<span class="json-number">${json}</span>`;
        } else if (typeof json === 'boolean' || json === null) {
            html += `<span class="json-literal">${json}</span>`;
        } else if (json instanceof Array) {
            if (json.length > 0) {
                html += '[<ol class="json-array">';
                json.forEach((item, i) => {
                    const newPath = `${path}[${i}]`;
                    html += `<li data-path="${newPath}">`;
                    if (isCollapsable(item)) html += '<a href class="json-toggle"><i class="fa-regular fa-square-plus"></i></a>';
                    html += json2html(item, options, newPath);
                    if (i < json.length - 1) html += ',';
                    html += '</li>';
                });
                html += '</ol>]';
            } else {
                html += '[]';
            }
        } else if (typeof json === 'object') {
            const keys = Object.keys(json);
            if (keys.length > 0) {
                html += '{<ul class="json-dict">';
                keys.forEach((key, i) => {
                    // const newPath = `${path}${key}`;
                    const newPath = `${path}${path ? '.' : ''}${key}`;
                    html += `<li data-path="${newPath}">`;
                    const keyRepr = `<span class="json-key">"${key}"</span>`;
                    if (isCollapsable(json[key])) {
                        html += `<a href class="json-toggle"><i class="fa-regular fa-square-plus"></i>${keyRepr}</a>`;
                    } else {
                        html += keyRepr;
                    }
                    html += `: ${json2html(json[key], options, newPath)}`;
                    if (i < keys.length - 1) html += ',';
                    html += '</li>';
                });
                html += '</ul>}';
            } else {
                html += '{}';
            }
        }
        return html;
    }

    $.fn.jsonViewer = function (json, options) {
        options = Object.assign({
            collapsed: false
        }, options);

        return this.each(function () {
            let html = json2html(json, options);
            if (isCollapsable(json)) {
                html = '<a href class="json-toggle"><i class="fa-regular fa-square-plus"></i></a>' + html;
            }
            $(this).html(html).addClass('json-document');

            $(this).off('click').on('click', 'a.json-toggle', function () {
                const target = $(this).toggleClass('collapsed').siblings('ul.json-dict, ol.json-array');
                target.toggle();
                if (target.is(':visible')) {
                    $(this).find('i').removeClass('fa-square-minus').addClass('fa-square-plus');
                    target.siblings('.json-placeholder').remove();
                } else {
                    $(this).find('i').removeClass('fa-square-plus').addClass('fa-square-minus');
                    const count = target.children('li').length;
                    const placeholder = `${count} ${count > 1 ? 'items' : 'item'}`;
                    target.after(`<a href class="json-placeholder">${placeholder}</a>`);
                }
                return false;
            }).on('click', 'a.json-placeholder', function () {
                $(this).siblings('a.json-toggle').click();
                return false;
            }).on('click', 'li', function (e) {
                e.stopPropagation();
                const path = $(this).data('path');
                const newPath = getPath(path)
                $('#path-display').text('路径：' + newPath);
                $('#path-info').show();
                $('#copy-path-btn').css('display', 'inline');
            });

            $('#copy-path-btn').off('click').on('click', function () {
                const path = $('#path-display').text().replace('路径：', '');

                const tempTextarea = document.createElement('textarea');
                tempTextarea.value = path;
                document.body.appendChild(tempTextarea);
                tempTextarea.select();
                document.execCommand('copy');
                document.body.removeChild(tempTextarea);
                Swal.fire({
                    icon: 'success',
                    toast: true,
                    position: 'top',
                    showConfirmButton: false,
                    timer: 3000,
                    title: '已复制到剪切板！',
                    width: '200',
                })
            });

            if (options.collapsed) {
                $(this).find('a.json-toggle').click();
            }
        });
    };
})(jQuery);

$(function () {
    $('#copy-json-btn').on('click', function () {
        let inputContent = $('#json-input').val().trim();
        inputContent = inputContent.replace(/([,{]\s*)'([^']+)'\s*:/g, '$1"$2":').replace(/:\s*'([^']*)'/g, ': "$1"').replace(/\bNone\b/g, 'null');
        const json = JSON.parse(inputContent);
        const formattedJson = JSON.stringify(json, null, 2);

        const tempTextarea = document.createElement('textarea');
        tempTextarea.value = formattedJson;
        document.body.appendChild(tempTextarea);
        tempTextarea.select();
        document.execCommand('copy');
        document.body.removeChild(tempTextarea);
        Swal.fire({
            icon: 'success',
            toast: true,
            position: 'top',
            showConfirmButton: false,
            timer: 3000,
            title: '已复制到剪切板！',
            width: '200',
        });
    });
});

$(document).ready(function () {
    const jsonContainer = $('#json_container');
    const btn = $('#fullscreen-btn');

    // 监听全屏状态变化
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
    document.addEventListener('msfullscreenchange', handleFullscreenChange);

    function handleFullscreenChange() {
        if (!document.fullscreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement) {
            // 退出全屏
            jsonContainer.removeClass('fullscreen'); // 取消自定义样式
            btn.html('<i class="fas fa-expand"></i> 全屏');
        }
    }

    btn.on('click', function () {
        // 检查是否在全屏模式
        if (document.fullscreenElement || document.webkitFullscreenElement || document.msFullscreenElement) {
            // 退出全屏
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        } else {
            // 进入全屏模式
            const element = document.documentElement; // 整个页面
            if (element.requestFullscreen) {
                element.requestFullscreen();
            } else if (element.webkitRequestFullscreen) {
                element.webkitRequestFullscreen();
            } else if (element.msRequestFullscreen) {
                element.msRequestFullscreen();
            }
            jsonContainer.addClass('fullscreen'); // 添加自定义样式
            btn.html('<i class="fas fa-compress"></i> 退出全屏');
        }
    });

    $(document).click(function (event) {
        if (!$(event.target).closest('#json-renderer').length) {
            $('#path-info').hide();
        }
    });
});
