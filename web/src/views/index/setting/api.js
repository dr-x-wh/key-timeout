import request from "@/utils/request.js";

export function useUpdate(data) {
    return request.patch('/user', data)
}
