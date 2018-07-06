import gql from 'graphql-tag'


export const ProblemDetail = gql`
    query( $pk: ID! ){
        problem( pk: $pk ){
            title,
            content,
            standardInput,
            standardOutput,
            constraints,
            resource,
            note,
            time_limit,
            memory_limit
        }
    }
`