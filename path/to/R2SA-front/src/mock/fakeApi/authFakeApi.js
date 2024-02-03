import { Response } from 'miragejs'
import uniqueId from 'lodash/uniqueId'
import isEmpty from 'lodash/isEmpty'

export default function authFakeApi (server, apiPrefix) {
    
    server.post(`${apiPrefix}/sign-in`, (schema, {requestBody}) => {
        const { user_name, password } = JSON.parse(requestBody)
        const user = schema.db.signInUserData.findBy({ accountuser_name: user_name, password })
        console.log('user', user)
        if (user) {
            const { avatar, user_name, email, authority } = user
            return {
                user: { avatar, user_name, email, authority },
                token: 'wVYrxaeNa9OxdnULvde1Au5m5w63'
            }
        }
        return new Response(401, { some: 'header' }, { message: `user_name: admin | password: 123Qwe` })
    })

    server.post(`${apiPrefix}/sign-out`, () => {
        return true
    })

    server.post(`${apiPrefix}/sign-up`, (schema, {requestBody}) => {
        const { user_name, password, email } = JSON.parse(requestBody)
        const userExist = schema.db.signInUserData.findBy({ accountuser_name: user_name })
        const emailUsed = schema.db.signInUserData.findBy({ email })
        const newUser = {
            avatar: '/img/avatars/thumb-1.jpg',
            user_name,
            email,
            authority: ['admin', 'user'],
        }
        if (!isEmpty(userExist)) {
            const errors = [
                {message: '', domain: "global", reason: "invalid"}
            ]
            return new Response(400, { some: 'header' }, { errors, message: 'User already exist!' })
        } 

        if (!isEmpty(emailUsed)) {
            const errors = [
                {message: '', domain: "global", reason: "invalid"}
            ]
            return new Response(400, { some: 'header' }, { errors, message: 'Email already used' })
        } 

        schema.db.signInUserData.insert({...newUser, ...{id: uniqueId('user_'), password, accountuser_name: user_name}})
        return {
            user: newUser,
            token: 'wVYrxaeNa9OxdnULvde1Au5m5w63'
        }
    })

    server.post(`${apiPrefix}/forgot-password`, () => {
        return true
    })

    server.post(`${apiPrefix}/reset-password`, () => {
        return true
    })
}