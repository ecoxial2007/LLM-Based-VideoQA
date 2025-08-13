# XD智问慧学

+ 该系统为西安电子科技大学计算机学院开发的教学课程视频自动检索、片段定位、问答系统。

+ 运行系统：Windows 10/11

+ 文件结构：
  前端：vue-project  —— Vue3+Vite+Element plus组件库

  后端：flask-project —— flask web框架

+ 运行：

## 前端：vue-project

下面是官方的README，在配置下面的环境前，还需要安装node.js (https://nodejs.org/en)

**官方README**

This template should help get you started developing with Vue 3 in Vite.

### 1. Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

### 2. Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/). （不用配）

### 3. Project Setup
+ cd 到 `./前端/vue-project` 后执行
```sh
pnpm install
```

#### Compile and Hot-Reload for Development

```sh
pnpm dev
```

#### Compile and Minify for Production

```sh
pnpm build
```

#### 可能会遇到的问题：

1. 不需要conda环境，首先conda deactivate出来
2. pnpm install报错：

+ 删除`node_modules`文件夹和`package-lock.json`(如果有的话)，重新运行`pnpm install`
+ 删除`package.json`文件，运行`pnpm init`

3. pnpm install装的很慢：全局配置淘宝镜像源

## 后端：flask-project

### 环境配置

进入conda环境，装个flask，openai，flask-session

## 运行：

+ cd到`./后端/flaskProject`后执行

~~~bash
python app.py
~~~

+ 再启动前端

~~~bash
pnpm dev
~~~



## 功能：

**参照后端的程序**  

登录功能的设置逻辑为：输入字符串不为空即跳转；也可以做一个简易的实现，用一个json文件维护用户名和密码，拿前端输入的做匹配，但生产环境中这样搞就是事故，因为可以通过爬虫等方法直接扒出用户数据。正常应该对数据库做密钥加密。
