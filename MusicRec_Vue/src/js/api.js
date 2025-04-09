import Fetch from './fetch'

// 初始化获取用户以及标签
export const initPage = () => Fetch('/api/index/login/', '', 'GET')
// 登录
export const getLogin = (loginInfo) => Fetch('/api/index/login/', loginInfo, 'POST')
// 获取主页分类数据
export const getHomeCategoriesData = (request) => Fetch('/api/index/home/', request, 'GET')
// 推荐模块
export const getRecommon = (request) => Fetch('/api/index/rec/', request, 'GET')
