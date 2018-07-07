import gql from 'graphql-tag'


export const ProblemList = gql`
    query problemList( $page: Int! ){
        problemList( page: $page ) {
            maxpage
            problemList{
                problemId,
                title,
                submit,
                accept,
            }
        }
    }
`