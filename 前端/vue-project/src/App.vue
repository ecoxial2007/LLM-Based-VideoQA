<!-- src/App.vue -->
<template>
    <div id="app">
        <router-view />
    </div>
</template>

<script>
export default {
    name: "App",
};
</script>

<style>
/* 隐藏 Webkit 浏览器的滚动条 */
::-webkit-scrollbar {
    width: 4px; /* 滚动条的宽度 */
}
/* 定义滑块样式 */
::-webkit-scrollbar-thumb {
    background-color: #888; /* 滑块颜色 */
    border-radius: 10px; /* 圆角 */
}

/* 定义滑块的悬停效果 */
::-webkit-scrollbar-thumb:hover {
    background-color: #555; /* 悬停时的颜色 */
}

/* 定义轨道样式 */
::-webkit-scrollbar-track {
    background: #f1f1f1; /* 轨道颜色 */
    border-radius: 10px; /* 圆角 */
}
.el-textarea__inner:focus {
    box-shadow: 0 0 0 1px #f56c6c inset !important;
}
</style>
