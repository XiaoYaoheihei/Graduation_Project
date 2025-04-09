import { createRouter, createWebHistory } from 'vue-router'; // 使用命名导入
import Home from '@/Page/Home.vue';
import Login from '@/Page/Login.vue'

const router = createRouter({
    history: createWebHistory(), // 使用 HTML5 历史模式
    routes: [
        {
            path: '/login',
            name: 'login',
            component: Login,
            meta: {
              needLogin: false
            }
        },
        {
          path: '/', // 根路径
          name: 'Home', // 路由名称
          component: Home, // 映射到 Home.vue 组件
          meta: {
            needLogin: true
          }
        }
    ]
})

router.beforeEach((to, from, next) => {
   if (to.meta.needLogin) {
    if (localStorage.getItem('username')) {
        next();
    } else {
        next({
            path: '/login',
            query: {redirect: to.fullPath}
        });
    }
   } else {
    next();
   }
});

export default router;