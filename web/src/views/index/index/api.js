import request from "@/utils/request.js"

export function useGetList(query) {
    return request.get('/info/list', {params: query})
}

export function useCreate(data) {
    return request.post('/info', data)
}

export function useDelete(info_id) {
    return request.delete(`/info/${info_id}`)
}
