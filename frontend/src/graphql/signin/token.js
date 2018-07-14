import gql from 'graphql-tag'

export const UserLogin = gql`
    mutation( $username: String! , $password: String! ){
        UserLogin(username: $username password: $password){
            token
        }
    }
`

export const verifyToken = gql`
    mutation( $token: String! ){
        verifyToken(token: $token){
            payload
        }
    }
`