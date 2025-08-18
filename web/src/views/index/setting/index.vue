<script setup>
import {onMounted, reactive, ref} from "vue";
import {getInfo} from "@/api/user.js";
import {useUpdate} from "./api.js";
import {ElMessage} from "element-plus";

const loading = ref(false)

const data = reactive({
  remind_time: null,
  phone: null,
})

const getData = async () => {
  try {
    loading.value = true
    const result = await getInfo()
    data.phone = result?.phone
    data.remind_time = result?.remind_time
  } catch (e) {
    console.warn(e)
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  try {
    loading.value = true
    await useUpdate(data)
    ElMessage.success("保存成功")
  } catch (e) {
    console.warn(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  getData()
})
</script>

<template>
  <div v-loading="loading"
       style="padding: 30px; display: flex; flex-direction: column; gap: 20px; align-items: center;">
    <el-form size="small" style="width: 300px;" :label-width="100">
      <el-form-item prop="remind_time" label="到期提醒时间">
        <el-time-picker value-format="HH:mm:ss" v-model="data.remind_time"/>
      </el-form-item>
      <el-form-item prop="phone" label="提醒电话">
        <el-input v-model="data.phone"/>
      </el-form-item>
      <el-form-item>
        <el-button @click="handleSave">保存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
</style>
