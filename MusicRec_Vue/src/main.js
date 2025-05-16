import { createApp } from 'vue'
import App from './App.vue'
import router from './route/index'

// 清除 localStorage 中的 username（仅测试时使用）
localStorage.removeItem('username');

const app = createApp(App)
app.use(router)
app.mount('#app')
