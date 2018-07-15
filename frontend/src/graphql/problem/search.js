import gql from 'graphql-tag'


export const ProblemListGQL = gql`
    query problemList( $page: Int! ){
        problemList( page: $page ) {
            problemId,
            title,
            submit,
            accept,
        }
    }
`