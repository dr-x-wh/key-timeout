// 路由守卫
import useUserStore from "@/store/user.js";

export default async function (to, from) {
    const userStore = useUserStore()
    if (userStore.getOnlineState()) {
        await userStore.getInfo()
        return true
    } else {
        if (to?.meta?.online === false) return true//
        else return {path: '/login'}//
    }
}
