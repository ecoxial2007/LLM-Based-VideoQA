<template>
    <Header :showInfo="true"></Header>
    <el-container class="container" style="height: 80vh">
        <!-- 左侧视频列表 -->
        <el-aside width="20%" class="aside-menu">
            <div class="logo">
                <h2>视频列表</h2>
            </div>
            <el-menu
                active-text-color="#ffd04b"
                background-color="#b0252a"
                text-color="#fff"
                @select="handleVideoSelect"
                :default-active="selectedVideo"
                class="el-menu-vertical-demo"
            >
                <el-menu-item
                    v-for="(name, key) in videos"
                    :key="key"
                    :index="key"
                >
                    <el-icon><video-camera /></el-icon>
                    <span>{{ name }}</span>
                </el-menu-item>
            </el-menu>
        </el-aside>

        <!-- 中间视频播放器 -->
        <el-container class="center-main">
            <el-main class="main-content">
                <div v-if="selectedVideo" class="video-container">
                    <div class="video-wrapper">
                        <video
                            ref="videoPlayer"
                            :src="`/api/video/${selectedVideo}.mp4`"
                            controls
                        ></video>
                        <div class="progress-container">
                            <div class="progress-label">知识点位置：</div>
                            <!-- 高亮进度条 -->
                            <div class="progress-bar">
                                <!-- 进度高亮区域 -->
                                <div
                                    class="progress-highlight"
                                    :style="progressHighlightStyle"
                                ></div>
                            </div>
                        </div>
                    </div>
                    <!--                     
                    <video
                        :src="`/api/video/${selectedVideo}.mp4`"
                        controls
                    ></video> -->
                </div>
                <div v-else class="placeholder">
                    <div class="video-int">
                        <h1>{{ videoTitle }}</h1>
                        <p>{{ videoDes }}</p>
                    </div>
                    <el-empty description="请选择一个视频进行播放"></el-empty>
                </div>
            </el-main>
        </el-container>

        <!-- 右侧聊天区域 -->
        <el-aside width="30%" class="aside-chat">
            <el-card class="chat-card">
                <h3>聊天区域</h3>
                <div class="chat-container">
                    <!-- 仅当有聊天记录时显示聊天历史 -->
                    <div v-if="chatHistory.length > 0" class="chat-history">
                        <div
                            v-for="(chat, index) in chatHistory"
                            :key="index"
                            class="chat-message"
                        >
                            <!-- 用户消息 -->
                            <div
                                v-if="chat.sender === 'user'"
                                class="message user-message"
                            >
                                <div class="message-content">
                                    {{ chat.content }}
                                </div>
                            </div>
                            <!-- 助手消息 -->
                            <div v-else class="message assistant-message">
                                <div class="message-content">
                                    {{ chat.content }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- 聊天输入区域 -->
                    <div class="chat-input-area">
                        <el-input
                            type="textarea"
                            v-model="question"
                            placeholder="请输入你的问题"
                            rows="3"
                            class="chat-input"
                        ></el-input>
                        <el-button
                            type="danger"
                            icon="Position"
                            @click="sendQuestion"
                            class="send-button"
                        >
                            发送
                        </el-button>
                    </div>
                </div>
            </el-card>
        </el-aside>
    </el-container>
</template>

<script>
import Header from "@/components/Header.vue";
import { ref, onMounted, watch, nextTick, computed } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
    name: "App",
    components: {
        Header,
    },
    setup() {
        const videos = ref({});
        const selectedVideo = ref("");
        const question = ref("");
        let videoTitle = ref("");
        let videoDes = ref("");
        const chatHistory = ref([]);
        const annotations = ref([]);
        const videoPlayer = ref(null);

        // 获取视频列表
        const fetchVideos = async () => {
            try {
                const response = await axios.get("/api/videos");
                videos.value = response.data;
                videoTitle.value = "欢迎来到万波老师的《C语言程序设计》课程";
                videoDes.value =
                    "这里有丰富的学习资源，你可以在左侧选择课程对应的章节，每个童节包含多个知识点，每个知识点下包含了多个对应点学习视频，学习过程中有任何疑问可以随时在右边进行提问哦。";
            } catch (error) {
                console.error("获取视频列表失败", error);
            }
        };

        // 重置对话历史
        const resetConversation = async () => {
            try {
                await axios.post(
                    "/api/reset-conversation",
                    {},
                    {
                        withCredentials: true, // 确保请求包含会话信息
                    }
                );
                chatHistory.value = [];
                annotations.value = [];
            } catch (error) {
                console.error("重置对话历史失败", error);
            }
        };

        // 处理视频选择
        const handleVideoSelect = async (key) => {
            selectedVideo.value = key;
            // 重置对话历史
            await resetConversation();
            // 清空聊天区域
            question.value = "";
        };

        // 发送问题
        const sendQuestion = async () => {
            if (!question.value) {
                ElMessage.warning("请输入问题。");
                return;
            }

            try {
                // 添加用户消息到聊天记录
                chatHistory.value.push({
                    sender: "user",
                    content: question.value,
                });

                // 发送请求前保存用户输入并清空输入框
                const userQuestion = question.value;
                question.value = "";

                const postData = {
                    question: userQuestion,
                };

                // 如果已选择视频，则添加视频名称
                if (selectedVideo.value) {
                    postData.video_name = selectedVideo.value;
                }

                const response = await axios.post(
                    "/api/gpt-response",
                    postData
                );

                // 检查后端返回的错误信息
                if (response.data.error) {
                    ElMessage.error(response.data.error);
                    return;
                }

                // 如果GPT返回了视频名称且未选择视频，自动选择该视频
                if (response.data.video_name && !selectedVideo.value) {
                    selectedVideo.value = response.data.video_name;
                }

                // 更新高亮时间戳
                if (response.data.annotations) {
                    console.log(response.data.annotations);
                    annotations.value = response.data.annotations.map(
                        (ann) => ({
                            start: ann.start,
                            end: ann.end > 1 ? 1 : ann.end,
                            color: ann.color || "#ff0000",
                        })
                    );
                }

                // 添加助手回复到聊天记录
                chatHistory.value.push({
                    sender: "assistant",
                    content: response.data.response,
                });
                // 自动滚动到聊天区域底部
                nextTick(() => {
                    const chatContainer =
                        document.querySelector(".chat-history");
                    if (chatContainer) {
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    }
                });
            } catch (error) {
                console.error("发送问题失败", error);
                if (
                    error.response &&
                    error.response.data &&
                    error.response.data.error
                ) {
                    ElMessage.error(error.response.data.error);
                } else {
                    ElMessage.error("发送问题失败，请稍后重试。");
                }
            }
        };

        // 计算属性，生成 progress-highlight 的样式
        const progressHighlightStyle = computed(() => {
            if (annotations.value.length === 0) {
                return {
                    width: "100%",
                    height: "100%",
                    backgroundColor: "#e0e0e0", // 默认背景色
                };
            }

            const stops = [];

            // 添加初始透明区域
            stops.push("transparent 0%");

            annotations.value.forEach((ann) => {
                let startPercent = (ann.start * 100).toFixed(2);
                let endPercent = (ann.end * 100).toFixed(2);

                // 确保高亮区域最小宽度，以便可见
                const minWidthPercent = 1; // 最小宽度（百分比）
                if (endPercent - startPercent < minWidthPercent) {
                    endPercent = parseFloat(startPercent) + minWidthPercent;
                    if (endPercent > 100) endPercent = 100;
                }

                // 添加透明区域和高亮区域
                stops.push(`transparent ${startPercent}%`);
                stops.push(`${ann.color} ${startPercent}%`);
                stops.push(`${ann.color} ${endPercent}%`);
                stops.push(`transparent ${endPercent}%`);
            });

            // 添加结束透明区域
            stops.push("transparent 100%");

            // 构建背景渐变
            const backgroundImage = `linear-gradient(to right, ${stops.join(
                ", "
            )})`;

            return {
                width: "100%",
                height: "100%",
                backgroundImage: backgroundImage,
                backgroundRepeat: "no-repeat",
            };
        });

        onMounted(() => {
            fetchVideos();
        });

        return {
            videoTitle,
            videoDes,
            videos,
            selectedVideo,
            question,
            chatHistory,
            annotations,
            videoPlayer,
            handleVideoSelect,
            sendQuestion,
            progressHighlightStyle,
        };
    },
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
/* 全局样式 */
.container {
    margin: 20px auto 0;
}
.el-container {
    width: 90%;
    background-color: #f5f7fa;
}

/* 左侧菜单样式 */
.aside-menu {
    background-color: #b0252a;
    color: rgba(255, 255, 255, 0.85);
    padding: 0;
    width: auto;
    max-width: 280px;
}

.logo {
    position: sticky;
    top: 0;
    z-index: 9;
    height: 60px;
    background-color: #b0252a;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    border-bottom: 1px solid #870b10;
}

.logo h2 {
    margin: 0;
    font-size: 20px;
}

.el-menu-vertical-demo {
    border-right: none;
}

.el-menu-item {
    color: rgba(255, 255, 255, 0.85) !important;
    border-bottom: 1px solid #870b10;
}

.el-menu-item:hover {
    background-color: #870b03 !important;
    color: #fff !important;
}

.el-menu-item.is-active {
    background-color: #870b03 !important;
    color: #fff !important;
}

.el-menu-item .el-icon {
    margin-right: 10px;
}

/* 中间内容区域 */
.main-content {
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ebeef5;
    border-right: none;
}

.video-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.video-container video {
    max-width: 100%;
    max-height: 100%;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.video-wrapper {
    position: relative;
}

.video-wrapper video {
    max-width: 100%;
    max-height: 100%;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.progress-container {
    margin-top: 10px;
}

.progress-label {
    font-weight: bold;
    margin-bottom: 10px;
}

.progress-bar {
    position: relative;
    width: 100%;
    height: 12px;
    background-color: #e0e0e0;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

.progress-highlight {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
}

.placeholder {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    height: 100%;
}
.placeholder .video-int {
}

.el-empty {
    flex: 1;
    /* margin-top: -100px; */
}

/* 右侧聊天区域 */
.aside-chat {
    /* border-left: 1px solid #ebeef5; */
}

.chat-card {
    height: 100%;
    display: flex;
    flex-direction: column;
    background-color: #fff;
    position: relative;
}

.chat-container {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.chat-history {
    flex: 1;
    margin-top: 20px;
    overflow-y: auto;
    padding: 10px;
    background-color: #fafafa;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    max-height: calc(80vh - 240px);
}

.chat-message {
    display: flex;
    margin-bottom: 10px;
}

.message {
    max-width: 70%;
    padding: 10px;
    border-radius: 10px;
    word-break: break-word;
}

.user-message {
    margin-left: auto;
    background-color: #f56c6c;
    color: #fff;
    border-bottom-right-radius: 0;
}

.assistant-message {
    margin-right: auto;
    background-color: #e8e8e8;
    color: #333;
    border-bottom-left-radius: 0;
}

.message-content {
    font-size: 14px;
    line-height: 1.5;
}

.chat-input-area {
    width: 90%;
    margin-top: 10px;
    margin-bottom: 10px;
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
}

.chat-input {
    width: 100%;
}

.send-button {
    margin-top: 10px;
    align-self: flex-end;
}

.el-divider {
    margin: 10px 0;
}
</style>
