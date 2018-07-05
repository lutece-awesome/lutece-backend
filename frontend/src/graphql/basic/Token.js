import gql from 'graphql-tag'

export const tokenAuthn = gql`
    mutation( $username: String! , $password: String! ){
        tokenAuth(username: $username password: $password){
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
export const verifyToken = gql`
    mutation( $token: String! ){
        refreshToken(token: $token){
            payload
        }
    }
`