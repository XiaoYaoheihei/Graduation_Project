import qs from 'qs';

const Fetch = async (url = '', data = {}, type = 'GET', headers) => {
    type = type.toUpperCase();
    let requestConfig = {
        method: type,
        headers: headers || {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        credentials: 'include', // 携带 Cookie（等效于 axios 的 withCredentials）
    };

    // 处理 GET 参数
    if (type === 'GET' && Object.keys(data).length !== 0) {
        url += `?${qs.stringify(data)}`;
    }

    // 处理 POST 数据
    if (type === 'POST') {
        requestConfig.body = qs.stringify(data);
    }

    try {
        const response = await fetch(url, requestConfig);
        // 检查 HTTP 状态码
        if (!response.ok) {
            const error = new Error(`HTTP Error: ${response.status}`);
            error.status = response.status;
            throw error;
        }
        return await response.json(); // 解析 JSON 数据
    } catch (err) {
        // 统一错误处理（模拟 axios 拦截器逻辑）
        if (err.status) {
            switch (err.status) {
                case 404:
                    err.message = '未找到指定文件!';
                    break;
                case 403:
                    err.message = '未授权，请登录';
                    break;
                default:
                    err.message = '获取失败!';
            }
        } else {
            err.message = '网络错误或请求被阻止';
        }
        throw err; // 抛出错误供上层捕获
    }
};

export default Fetch;