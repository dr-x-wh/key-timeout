import axios from "axios";
import {ElMessage} from "element-plus";

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
    ElMessage.error(error?.response?.data?.message || '网络异常')
    return Promise.reject(error)
})

export default request
