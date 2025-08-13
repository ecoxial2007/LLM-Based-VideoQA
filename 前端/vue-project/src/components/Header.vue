<template>
    <header>
        <div class="container">
            <router-link to="/">
                <img src="@/assets/images/logo.png" alt="" />
            </router-link>
            <el-dropdown v-show="showInfo">
                <div class="user-info">
                    {{ userInfo && userInfo.username }}，你好
                    <el-icon class="el-icon--right">
                        <arrow-down />
                    </el-icon>
                </div>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item @click="exit">退出</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </header>
</template>
<script setup>
import { reactive } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";
import { useRouter } from "vue-router";
const router = useRouter();

defineProps({
    showInfo: {
        type: Boolean,
        default: false,
    },
});

// 获取用户名
let userInfo = localStorage.getItem("videoUserInfo");
userInfo = reactive(userInfo ? JSON.parse(userInfo) : null);

const exit = () => {
    ElMessageBox.confirm("你确定要退出吗？", "确认退出", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
    })
        .then(() => {
            localStorage.removeItem("videoUserInfo");
            // 回到登录
            router.push("/login");
        })
        .catch(() => {
            // 用户点击取消
            ElMessage({
                type: "info",
                message: `已取消`,
            });
        });
};
</script>
<style scoped>
:deep(.el-tooltip__trigger:focus-visible) {
    outline: unset;
}
header {
    box-shadow: 0 2px 5px rgba(137, 5, 10, 0.26);
    background-color: #fff;
}
header .container {
    height: 100px;
    width: 80%;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
header .container img {
    height: 50px;
}
header .container .user-info {
    cursor: pointer;
}
</style>
