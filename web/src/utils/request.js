import axios from "axios";
import {ElMessage} from "element-plus";
import useUserStore from "@/store/user.js";
import router from "@/router/index.js";

const request = axios.create({
    baseURL: '/api', timeout: 30000,
})

request.interceptors.request.use(async (config) => {
    const token = localStorage.getItem('token')
    if (token) config.headers['Authorization'] = `Bearer ${token}`
    return config
}, async (error) => {
    return Promise.reject(error)
})
request.interceptors.response.use(async (response) => {
    return response?.data?.data
}, async (error) => {
    (httpErrorMap?.[error.status] || httpErrorMap.other)?.(error?.response?.data?.message)
    return Promise.reject(error)
})

const httpErrorMap = {
    401: async (msg) => {
        useUserStore().cleanOnline()
        await router.push({path: '/login'})
    },//
    other: (msg) => {
        ElMessage.error(msg)
    },//
}

export default request
