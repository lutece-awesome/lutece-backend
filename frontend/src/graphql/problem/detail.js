import gql from 'graphql-tag'

export const ProblemDetailGQL = gql`
    query( $slug: String! ){
        problem( slug: $slug ){
            title,
            content,
            standardInput,
            standardOutput,
            constraints,
            resource,
            note,
            timeLimit,
            memoryLimit
        }
    }
`
