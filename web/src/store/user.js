import {defineStore} from "pinia";
import {getInfo, login, logout} from "@/api/user.js";

const useUserStore = defineStore('user', {
    state: () => ({
        id: null, username: null,
    }),//
    getters: {},//
    actions: {
        async login(username, password) {
            const result = await login({username, password})
            localStorage.setItem("token", result)
            await this.getInfo()
        },//
        async logout() {
            try {
                await logout()
            } finally {
                this.id = null
                this.username = null
                localStorage.removeItem("token")
            }
        },//
        async getInfo() {
            const userInfo = await getInfo()
            this.id = userInfo.id
            this.username = userInfo.username
        },//
        getOnlineState() {
            return !!localStorage.getItem("token")
        },
    },//
})

export default useUserStore
