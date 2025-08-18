<script setup>
import {onMounted, reactive, ref} from "vue";
import useUserStore from "@/store/user.js";
import {useRoute, useRouter} from "vue-router";
import {ElMessage} from "element-plus";

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const formRef = ref()

const loading = ref(false)

const form = reactive({
  username: null,
  password: null,
})

const rules = reactive({
  username: [
    {required: true, message: '请输入用户名', trigger: 'blur'},
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
  ],
})

const handleLogin = async () => {
  try {
    loading.value = true
    if (formRef.value) {
      const valid = await formRef.value.validate()
      if (valid) {
        await userStore.login(form.username, form.password)
        await router.push({path: '/'})
      }
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (route.query?.message) ElMessage.warning(route.query.message)
})
</script>

<template>
  <div class="login-body">
    <el-card style="width: 500px;">
      <template #header>
        <div style="text-align: center; font-size: 24px; font-weight: bold;">登录</div>
      </template>
      <div v-loading="loading">
        <el-form ref="formRef" :rules="rules" label-position="top" :model="form" :label-width="60">
          <el-form-item label="用户名" prop="username">
            <el-input :validate-event="false" @keydown.enter="handleLogin" v-model="form.username"/>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input :validate-event="false" @keydown.enter="handleLogin" type="password" v-model="form.password"/>
          </el-form-item>
          <el-form-item>
            <el-button style="width: 100%; margin-top: 15px;" size="large" @click="handleLogin">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.login-body {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  justify-content: space-evenly;
}
</style>
