// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import { ElMessage } from "element-plus";

import Login from "@/views/Login.vue";
import Video from "@/views/Video.vue";

const routes = [
    {
        path: "/",
        redirect: "/video",
    },
    {
        path: "/login",
        name: "Login",
        meta: {
            title: "登录",
            needLogin: false,
        },
        component: Login,
    },
    {
        path: "/video",
        name: "Video",
        meta: {
            title: "课程学习",
            needLogin: true,
        },
        component: Video,
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
    const getUserInfo = () => {
        const userInfo = localStorage.getItem("videoUserInfo");
        return userInfo ? JSON.parse(userInfo) : null;
    };
    const userInfo = getUserInfo();
    document.title = to.meta.title || "视频问答";

    // 如果是登录页并且用户已登录，重定向到功能页
    if (to.path === "/login") {
        if (userInfo && userInfo.username) {
            return next({ path: "/video" });
        }
    }

    // 检查是否需要登录
    if (to.meta.needLogin) {
        if (userInfo && userInfo.username) {
            return next();
        } else {
            ElMessage({
                message: "请登录",
                type: "warning",
            });
            return next({ path: "/login" });
        }
    }

    next();
});
export default router;
