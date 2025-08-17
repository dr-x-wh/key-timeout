<script setup>
import {computed, ref} from "vue";
import {useCreate, useGetDetail, useUpdate} from "@/views/index/index/api.js";

const loading = ref(false)
const visible = ref(false)
const type = ref(null)
const modalRef = ref()
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
  start_date: null,
  end_date: null,
})

const open = (typeVal, idVal) => {
  return new Promise((resolve) => {
    resolveRef = resolve
    if (typeVal === 'update') getData()
    type.value = typeVal
    visible.value = true
  })
}

const close = () => {
  data.value = {
    name: null,
    person: null,
    phone: null,
    start_date: null,
    end_date: null,
  }
}

const getData = async (info_id) => {
  const result = await useGetDetail(info_id)
  console.log(result)
}

const handleSave = async () => {
  if (type.value === 'add') await useCreate(data.value)
  else if (type.value === 'update') await useUpdate(data.value)
  if (modalRef.value) modalRef.value.handleClose()
  resolveRef()
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
    <div v-loading="loading">
      <el-form :label-width="70">
        <el-row :gutter="10">
          <el-col :span="12">
            <el-form-item prop="name" label="名称">
              <el-input v-model="data.name"/>
            </el-form-item>
          </el-col>
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
          <el-col :span="12">
            <el-form-item prop="start_date" label="开始日期">
              <el-date-picker type="date" value-format="YYYY-MM-DD" v-model="data.start_date"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item prop="end_date" label="到期日期">
              <el-date-picker type="date" value-format="YYYY-MM-DD" v-model="data.end_date"/>
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
