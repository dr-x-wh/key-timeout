<script setup>
import {computed, ref} from "vue";
import {useCreate, useGetDetail, useUpdate} from "@/views/index/index/api.js";
import {ElMessage} from "element-plus";

const loading = ref(false)
const visible = ref(false)
const type = ref(null)
const modalRef = ref()
const formRef = ref()
let resolveRef

const title = computed(() => {
  if (type.value === 'add') return '添加'
  else if (type.value === 'update') return '修改'
  else return '未知'
})

const data = ref({
  name: null,
  person: null,
  phone: null,
  date: null,
})

const rules = ref({
  name: [
    {required: true, message: '请输入名称', trigger: 'blur'},
  ],
  date: [
    {required: true, message: '请选择开始日期', trigger: 'change'},
  ],
})

const open = (typeVal, idVal) => {
  return new Promise((resolve) => {
    resolveRef = resolve
    if (typeVal === 'update') getData(idVal)
    type.value = typeVal
    visible.value = true
  })
}

const close = () => {
  data.value = {
    name: null,
    person: null,
    phone: null,
    date: null,
  }
  if (formRef.value) formRef.value.clearValidate()
}

const getData = async (info_id) => {
  try {
    loading.value = true
    const result = await useGetDetail(info_id)
    data.value = result
    data.value.date = [result?.start_date, result?.end_date]
  } catch (e) {
    console.warn(e)
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  try {
    if (type.value === 'add') await useCreate(data.value)
    else if (type.value === 'update') await useUpdate(data.value)
    ElMessage.success("保存成功")
    if (modalRef.value) modalRef.value.handleClose()
    resolveRef()
  } catch (e) {
    console.warn(e)
  }

}

defineExpose({
  open,
})
</script>

<template>
  <el-dialog ref="modalRef" v-model="visible" @closed="close">
    <template #header>
      <el-text size="large">{{ title }}</el-text>
    </template>
    <div v-loading="loading" style="padding: 0 20px;">
      <el-form ref="formRef" :rules="rules" :model="data" :label-width="110">
        <el-row :gutter="10">
          <el-col :span="12">
            <el-form-item prop="name" label="提醒任务名称">
              <el-input v-model="data.name"/>
            </el-form-item>
          </el-col>
        </el-row>
        <el-divider/>
        <el-row :gutter="10">
          <el-col :span="12">
            <el-form-item prop="person" label="联系人">
              <el-input v-model="data.person"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item prop="phone" label="联系电话">
              <el-input v-model="data.phone"/>
            </el-form-item>
          </el-col>
        </el-row>
        <el-divider/>
        <el-row :gutter="10">
          <el-col :span="12">
            <el-form-item prop="start_date" label="起止日期">
              <el-date-picker style="width: 100%;" type="daterange" value-format="YYYY-MM-DD" v-model="data.date"/>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </div>
    <template #footer>
      <el-button @click="handleSave" type="primary">保存</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
</style>
