import gql from 'graphql-tag'

export const ProblemListGQL = gql`
    query problemList( $page: Int! ){
        problemList( page: $page ) {
            maxpage
            problemList{
                problemId,
                title,
                submit,
                accept,
                slug,
            }
        }
    }
`
