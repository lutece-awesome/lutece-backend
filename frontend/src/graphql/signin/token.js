import gql from 'graphql-tag'

export const tokenAuth = gql`
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