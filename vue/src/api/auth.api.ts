import {http} from "./http"


export const getToken = (username: string, password: string) => {
    return http.post(
        "/token/",
        {
            "username": username,
            "password": password
        },
        {
            headers: {
                "Content-Type": "application/json"
            }
        }
    )
}

export const refreshToken = (refreshToken: string) => {
    return http.post(
        "/token/",
        {
            "refresh": refreshToken
        },
        {
            headers: {
                "Content-Type": "application/json"
            }
        }
    )
}