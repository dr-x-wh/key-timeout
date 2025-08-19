import {defineStore} from "pinia";
import {useGetInfo, useLogin, useLogout} from "@/api/user.js";

const useUserStore = defineStore('user', {
    state: () => ({
        id: null, username: null,
    }),//
    getters: {},//
    actions: {
        async login(username, password) {
            const result = await useLogin({username, password})
            localStorage.setItem("token", result)
            await this.getInfo()
        },//
        async logout() {
            try {
                await useLogout()
            } finally {
                this.cleanOnline()
            }
        },//
        cleanOnline() {
            this.id = null
            this.username = null
            localStorage.removeItem("token")
        },//
        async getInfo() {
            const userInfo = await useGetInfo()
            this.id = userInfo.id
            this.username = userInfo.username
        },//
        getOnlineState() {
            return !!localStorage.getItem("token")
        },
    },//
})

export default useUserStore
