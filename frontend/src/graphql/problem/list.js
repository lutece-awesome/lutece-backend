import gql from 'graphql-tag'


export const ProblemList = gql`
    query( $page: Int! ){
        problemList( page: $page ){
            problemId,
            title,
            submit,
            accept,
        }
    }
`