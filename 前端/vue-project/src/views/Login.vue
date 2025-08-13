<template>
    <div class="container">
        <Header></Header>
        <div class="login-box">
            <div class="login-form">
                <div class="inp">
                    <span>学号</span>：
                    <input type="text" v-model="username" />
                </div>
                <div class="inp">
                    <span>密码</span>：
                    <input type="password" v-model="password" />
                </div>
                <div class="submit-btn" @click="submitLogin">登录</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Header from "@/components/Header.vue";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
// 定义响应式变量
const username = ref("");
const password = ref("");
const router = useRouter();

// 登录处理函数
const submitLogin = () => {
    if (!username.value) {
        ElMessage({
            message: "用户名不能为空",
            type: "warning",
        });
        return;
    }
    if (!password.value) {
        ElMessage({
            message: "密码不能为空",
            type: "warning",
        });
        return;
    }
    let userInfo = {
        username: username.value,
        password: password.value,
    };
    localStorage.setItem("videoUserInfo", JSON.stringify(userInfo));
    ElMessage({
        message: "登录成功",
        type: "success",
    });
    router.push("/video");
};
</script>

<style scoped>
.container {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background-color: #ccc;
    background: url("@/assets/images/login_bg.png") no-repeat top center / cover;
}
.container .login-box {
    width: 424px;
    height: 482px;
    background: url("@/assets/images/login_box_bg.png") no-repeat center;
    background-size: 100% 100%;
    position: fixed;
    right: 10%;
    top: 60%;
    transform: translate(0, -50%);
}
.container .login-box .login-form {
    width: 80%;
    margin: 0 auto;
    position: absolute;
    top: 40%;
    left: 50%;
    transform: translateX(-50%);
}
.container .login-box .login-form .inp {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}
.container .login-box .login-form .inp span {
    width: 60px;
    text-align-last: justify;
    color: #666;
}
.container .login-box .login-form .inp input {
    flex: 1;
    height: 42px;
    margin-left: 10px;
    background: #fff;
    border: 1px solid #cccccc;
    border-radius: 8px;
    outline: none;
    padding-left: 5px;
}
.container .login-box .login-form .submit-btn {
    cursor: pointer;
    width: 182px;
    height: 42px;
    margin: 10px auto 0;
    text-align: center;
    line-height: 42px;
    background-color: #b0252a;
    border: 0;
    outline: none;
    font-size: 16px;
    color: #fff;
    border-radius: 5px;
    box-shadow: 0 0 9px rgba(0, 0, 0, 0.52);
}
</style>
