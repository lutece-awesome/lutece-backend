<template>
    <v-data-table :items = "problemItem"  :headers = "headers" hide-actions >
        <template slot="items" slot-scope = "props">
            <router-link tile tag="tr" :to='{name: "ProblemDetail", params: {slug: props.item.slug}}' :style="{cursor: 'pointer'}">
                <td class="text-xs-center">{{ props.item.problemId }}</td>
                <td class="text-xs-center">{{ props.item.title }}</td>
                <td class="text-xs-center">{{ props.item.accept }} / {{ props.item.submit }}</td>
                <td class="text-xs-center">{{ props.item.submit ? ( ( props.item.accept / props.item.submit ) * 100 ).toFixed( 2 ) : '0.00' }}%  </td>
            </router-link>
        </template>
    </v-data-table>
</template>


<script>
    export default {
        props:{
            problemItem:{
                type: Array,
                default : []
            }
        },
        data: () => ({
            hidden: false,
            headers:[
                {
                    text: '#',
                    align: 'center',
                    sortable: false,
                },
                {
                    text: 'Title',
                    align: 'center',
                    sortable: false,
                },
                {
                    text: 'Accepted / Submit',
                    align: 'center',
                    sortable: false,
                    class: 'hidden-sm-and-down'
                },
                {
                    text: 'A / S',
                    align: 'center',
                    sortable: false,
                    class: 'hidden-md-and-up'
                },
                {
                    text: 'Ratio',
                    align: 'center',
                    sortable: false
                }
            ]
        }),

        methods:{
            click: function(){
                alert( "click" );
            }
        }
    }
</script>

