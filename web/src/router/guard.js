// 路由守卫
import useUserStore from "@/store/user.js";

export default async function (to, from) {
    const userStore = useUserStore()
    if (userStore.getOnlineState()) {
        try {
            await userStore.getInfo()
            return true
        } catch (e) {
            await userStore.logout()
            return {name: 'login'}
        }
    } else {
        if (to?.meta?.online === false) return true//
        else return {name: 'login'}//
    }
}
