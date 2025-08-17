import request from "@/utils/request.js"

export function login(data) {
    return request.post('/login', data)
}

export function logout(data) {
    return request.post('/logout', data)
}

export function getInfo() {
    return request.get('/user/info')
}
