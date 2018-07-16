import gql from 'graphql-tag'

export const ProblemSearchGQL = gql`
    query( $title: String! ){
        problemsearch( title: $title){
            title,
            slug,
        }
    }
`
