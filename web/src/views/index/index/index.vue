<script setup>
import {onMounted, reactive, ref, toRefs} from "vue"
import {useGetList} from "./api.js"
import DetailModal from "@/views/index/index/DetailModal.vue";

const loading = ref(false)
const detailRef = ref()

const data = reactive({
  query: {
    page: 1, per_page: 10,
    name: null,
    person: null,
    phone: null,
    start_date: null,
    end_date: null,
  },
  list: [],
  total: null,
})

const {query, list, total} = toRefs(data)


const getList = async () => {
  try {
    loading.value = true
    const result = await useGetList(query.value)
    total.value = result.total
    list.value = result.data
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  query.value = {
    page: 1, per_page: 10,
    name: null,
    person: null,
    phone: null,
    start_date: null,
    end_date: null,
  }
  getList()
}

const handleDetail = (e, id) => {
  if (detailRef.value) {
    detailRef.value.open(e.target.dataset?.type, id).then(() => getList())
  }
}

onMounted(() => {
  getList()
})
</script>

<template>
  <div v-loading="loading" style="padding: 30px; display: flex; flex-direction: column; gap: 20px;">
    <el-form :label-width="70">
      <el-row :gutter="10">
        <el-col :span="4">
          <el-form-item prop="name" label="名称">
            <el-input v-model="query.name"/>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item prop="person" label="联系人">
            <el-input v-model="query.person"/>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item prop="phone" label="联系电话">
            <el-input v-model="query.phone"/>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item prop="start_date" label="开始日期">
            <el-date-picker type="daterange" v-model="query.start_date"/>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item prop="end_date" label="到期日期">
            <el-date-picker type="daterange" v-model="query.end_date"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col>
          <el-form-item>
            <el-button type="primary" @click="getList">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div><el-button icon="Plus" data-type="add" @click="handleDetail">添加</el-button></div>
    <el-table :data="list">
      <el-table-column label="序号" type="index"/>
      <el-table-column prop="name" label="名称"/>
      <el-table-column prop="person" label="联系人"/>
      <el-table-column prop="phone" label="联系电话"/>
      <el-table-column prop="start_date" label="开始日期"/>
      <el-table-column prop="end_date" label="到期日期"/>
      <el-table-column label="操作">
        <template #default="{row}">
          <el-button data-type="update" @click="(e) => handleDetail(e, row?.id)">修改</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination layout="total, prev, pager, next, ->, sizes, jumper" v-model:page-size="query.per_page"
                   v-model:current-page="query.page" :total="total"
                   @change="getList"/>
    <DetailModal ref="detailRef"/>
  </div>
</template>

<style scoped>
</style>
