import gql from 'graphql-tag'

export const LoginGQL = gql`
    mutation login( $username: username , $password: password ){
        login( username : $username , password: $password ){
            authed
        }
    }
`