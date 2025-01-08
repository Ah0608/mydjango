function parseUrlParams(url) {
    console.log('开始解析URL:', url);
    try {
        // 移除URL开头的@符号
        url = url.replace(/^@/, '');
        console.log('移除@后的URL:', url);

        // 直接提取查询字符串
        const queryStringMatch = url.match(/\?(.*)/);
        if (!queryStringMatch) {
            console.log('未找到查询字符串');
            return {};
        }

        const queryString = queryStringMatch[1];
        console.log('提取的查询字符串:', queryString);

        const params = {};

        // 手动解析查询字符串
        queryString.split('&').forEach((pair, index) => {
            console.log(`处理第${index + 1}个参数对:`, pair);
            const [key, value] = pair.split('=');
            if (key && value !== undefined) {
                try {
                    // 先进行 URL 解码
                    const decodedValue = decodeURIComponent(value);

                    // 尝试解析 JSON 字符串
                    try {
                        const jsonValue = JSON.parse(decodedValue);
                        params[key] = jsonValue;
                        console.log(`成功解析JSON参数 ${key}:`, jsonValue);
                    } catch (jsonError) {
                        // 如果不是有效的 JSON，则使用原始解码值
                        params[key] = decodedValue;
                        console.log(`非JSON参数 ${key}:`, decodedValue);
                    }
                } catch (e) {
                    params[key] = value;
                    console.log(`解码失败，使用原始值 ${key}:`, value);
                }
            }
        });

        console.log('解析完成，参数对象:', params);
        return params;
    } catch (error) {
        console.error('解析过程中发生错误:', error);
        throw new Error('无法解析URL参数');
    }
}

function compareParams(params1, params2) {
    const allKeys = new Set([...Object.keys(params1), ...Object.keys(params2)]);
    const differences = [];

    allKeys.forEach(key => {
        if (!(key in params1)) {
            differences.push({
                key,
                type: 'missing',
                side: 'left',
                value1: undefined,
                value2: params2[key]
            });
        } else if (!(key in params2)) {
            differences.push({
                key,
                type: 'missing',
                side: 'right',
                value1: params1[key],
                value2: undefined
            });
        } else if (params1[key] !== params2[key]) {
            differences.push({
                key,
                type: 'different',
                value1: params1[key],
                value2: params2[key]
            });
        }
    });

    return differences;
}

function compareValues(value1, value2) {
    // 如果两个值都是对象或数组
    if (typeof value1 === 'object' && value1 !== null &&
        typeof value2 === 'object' && value2 !== null) {
        return JSON.stringify(value1) === JSON.stringify(value2);
    }
    // 其他情况直接比较
    return value1 === value2;
}

function formatValue(value) {
    if (typeof value === 'object' && value !== null) {
        return JSON.stringify(value);
    }
    return value;
}

function generateComparisonTable(urlPair, index) {
    const {url1, url2, parsed1, parsed2, differences} = urlPair;

    let html = `
                <div class="params-comparison">
                    <table class="params-table">
                        <tr class="url-row">
                            <td colspan="3">URL对比 #${index + 1}</td>
                        </tr>
                        <tr>
                            <th>参数名</th>
                            <th>左侧值</th>
                            <th>右侧值</th>
                        </tr>`;

    const allParams = new Set([
        ...Object.keys(parsed1 || {}),
        ...Object.keys(parsed2 || {})
    ]);

    allParams.forEach(param => {
        const hasValue1 = parsed1 && (param in parsed1);
        const hasValue2 = parsed2 && (param in parsed2);
        const value1 = hasValue1 ? parsed1[param] : undefined;
        const value2 = hasValue2 ? parsed2[param] : undefined;

        let className, leftDisplay, rightDisplay;

        if (!hasValue1 && hasValue2) {
            className = 'param-missing';
            leftDisplay = '<span style="color: #dc3545; font-weight: bold;">【左侧缺失】</span>';
            rightDisplay = `<span>${formatValue(value2)}</span>`;
        } else if (hasValue1 && !hasValue2) {
            className = 'param-missing';
            leftDisplay = `<span>${formatValue(value1)}</span>`;
            rightDisplay = '<span style="color: #dc3545; font-weight: bold;">【右侧缺失】</span>';
        } else if (!compareValues(value1, value2)) {
            className = 'param-diff';
            leftDisplay = `<span class="diff-highlight">${formatValue(value1)}</span>`;
            rightDisplay = `<span class="diff-highlight">${formatValue(value2)}</span>`;
        } else {
            className = '';
            leftDisplay = `<span>${formatValue(value1)}</span>`;
            rightDisplay = `<span>${formatValue(value2)}</span>`;
        }

        html += `
                    <tr${className ? ` class="${className}"` : ''}>
                        <td>${param}</td>
                        <td>${leftDisplay}</td>
                        <td>${rightDisplay}</td>
                    </tr>`;
    });

    html += `</table></div>`;
    return html;
}

function compareURLs() {
    console.log('开始比较URLs');
    const urls1 = document.getElementById('url1').value.trim().split('\n');
    const urls2 = document.getElementById('url2').value.trim().split('\n');
    const resultDiv = document.getElementById('result');

    console.log('左侧URLs数量:', urls1.length);
    console.log('右侧URLs数量:', urls2.length);

    if (!urls1[0] || !urls2[0]) {
        resultDiv.innerHTML = '请在两侧都输入URL';
        resultDiv.className = 'not-match';
        return;
    }

    try {
        const normalizedUrls1 = urls1.filter(url => url.trim()).map(url => url.trim());
        const normalizedUrls2 = urls2.filter(url => url.trim()).map(url => url.trim());

        if (normalizedUrls1.length !== normalizedUrls2.length) {
            resultDiv.innerHTML = `❌ URL数量不匹配！左侧：${normalizedUrls1.length}个，右侧：${normalizedUrls2.length}个`;
            resultDiv.className = 'not-match';
            return;
        }

        let allMatch = true;
        let comparisonResults = '';

        // 比较每对URL
        const urlPairs = normalizedUrls1.map((url1, i) => {
            const url2 = normalizedUrls2[i];
            try {
                const parsed1 = parseUrlParams(url1);
                const parsed2 = parseUrlParams(url2);

                // 只比较参数是否有差异，不比较原始URL字符串
                const hasDifferences = Object.keys(parsed1).some(key => {
                    if (!(key in parsed2)) return true;
                    return !compareValues(parsed1[key], parsed2[key]);
                }) || Object.keys(parsed2).some(key => !(key in parsed1));

                if (hasDifferences) {
                    allMatch = false;
                }

                return {url1, url2, parsed1, parsed2, differences: []};
            } catch (error) {
                console.error(`处理第${i + 1}对URL时出错:`, error);
                throw error;
            }
        });

        // 生成比较结果HTML
        urlPairs.forEach((pair, index) => {
            comparisonResults += generateComparisonTable(pair, index);
        });

        // 显示总体结果和详细比较
        resultDiv.innerHTML = `
                    <div class="${allMatch ? 'match' : 'not-match'}">
                        ${allMatch ? '✅ 所有URL完全匹配！' : '❌ URL存在差异！'}
                    </div>
                    ${comparisonResults}`;

    } catch (error) {
        console.error('比较过程中发生错误:', error);
        resultDiv.innerHTML = '请确保输入的都是有效的URL';
        resultDiv.className = 'not-match';
    }
}

// 添加复制功能函数
async function copyToClipboard(button, elementId) {
    const text = document.getElementById(elementId).textContent;
    try {
        await navigator.clipboard.writeText(text);
        const originalText = button.textContent;
        button.textContent = '已复制！';
        button.style.backgroundColor = '#28a745';
        setTimeout(() => {
            button.textContent = originalText;
            button.style.backgroundColor = '#6c757d';
        }, 2000);
    } catch (err) {
        console.error('复制失败:', err);
        button.textContent = '复制失败';
        button.style.backgroundColor = '#dc3545';
        setTimeout(() => {
            button.textContent = '复制';
            button.style.backgroundColor = '#6c757d';
        }, 2000);
    }
}

function showParamsJson(side) {
    const textarea = document.getElementById(`url${side}`);
    const urls = textarea.value.trim().split('\n').filter(url => url.trim());

    if (!urls.length) {
        alert('请先输入URL');
        return;
    }

    try {
        // 只处理第一个URL
        const url = urls[0].replace(/^@/, '');
        const queryString = url.split('?')[1];
        if (!queryString) {
            alert('URL没有参数');
            return;
        }

        const params = parseUrlParams(url);

        const modal = document.getElementById('paramsModal');
        const modalContent = document.getElementById('modalContent');
        const modalTitle = document.getElementById('modalTitle');

        modalTitle.textContent = `URL参数 (${side === 1 ? '左侧' : '右侧'})`;
        // 直接显示参数对象
        modalContent.textContent = JSON.stringify(params, null, 2);
        modal.style.display = 'block';
    } catch (error) {
        console.error('处理URL时出错:', error);
        alert('参数解析失败');
    }
}

function closeModal() {
    document.getElementById('paramsModal').style.display = 'none';
}

function copyModalContent() {
    const content = document.getElementById('modalContent').textContent;
    navigator.clipboard.writeText(content)
        .then(() => {
            const copyBtn = document.querySelector('.modal-content .copy-button');
            copyBtn.textContent = '已复制！';
            copyBtn.style.backgroundColor = '#28a745';
            setTimeout(() => {
                copyBtn.textContent = '复制JSON数据';
                copyBtn.style.backgroundColor = '#6c757d';
            }, 2000);
        })
        .catch(err => {
            alert('复制失败');
        });
}

// 点击模态框外部关闭
window.onclick = function (event) {
    const modal = document.getElementById('paramsModal');
    if (event.target === modal) {
        closeModal();
    }
}