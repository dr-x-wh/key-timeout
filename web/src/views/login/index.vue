<script setup>
import {reactive} from "vue";
import useUserStore from "@/store/user.js";
import {getInfo} from "@/api/user.js";

const userStore = useUserStore()

const form = reactive({
  username: null,
  password: null,
})

const handleLogin = async () => {
  await userStore.login(form.username, form.password)
}

const handleLogout = async () => {
  await userStore.logout()
}

const handleGetInfo = async () => {
  await getInfo()
}
</script>

<template>
  <div class="login-body">
    <el-card style="width: 500px;">
      <el-form :model="form" :label-width="100">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username"/>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password"/>
        </el-form-item>
        <el-form-item label="" prop="password">
          <el-button @click="handleLogin">登录</el-button>
          <el-button @click="handleLogout">退出登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-button @click="handleGetInfo">查询</el-button>
  </div>
</template>

<style scoped>
.login-body {
  width: 100vw;
  height: 100vh;
  display: flex;
  gap: 20px;
  align-items: center;
  justify-content: space-evenly;
}
</style>
