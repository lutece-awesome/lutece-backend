<template>
    <v-layout row wrap justify-center>
        <v-flex xs12 md10 xl8 class='ma-2'>
            <h1>A PLUS B</h1>
        </v-flex>
        <v-flex xs12 md10 xl8>
            <v-tabs v-model="tabs" color="transparent">
                <v-tab>Description</v-tab>
                <v-tab>Editor</v-tab>
                <v-tab>Discussion</v-tab>
            </v-tabs>
        </v-flex>
        <v-flex xs12 md10 xl8 class='mt-2'>
            <v-tabs-items v-model="tabs">
                <v-tab-item>
                    <v-layout row wrap class='ma-1'>
                        <v-flex xs12 class='mb-2'>
                            <div class='headline my-2'>Content</div>
                            <v-card>
                                <v-card-text>输入两个整数,输出它们的和</v-card-text>
                            </v-card>
                        </v-flex>
                        <v-flex xs12 class='mb-2'>
                            <div class='headline my-2'>Standard Input</div>
                            <v-card>
                                <v-card-text>输入只有一行，包含两个整数a和b.</v-card-text>
                            </v-card>
                        </v-flex>
                        <v-flex xs12 class='mb-2'>
                            <div class='headline my-2'>Standard Output</div>
                            <v-card>
                                <v-card-text>输出a + b</v-card-text>
                            </v-card>
                        </v-flex>
                        <v-flex xs12 class='mb-2'>
                            <div class='headline my-2'>Constraints</div>
                            <v-card>
                                <v-card-text>0≤a,b≤100000</v-card-text>
                            </v-card>
                        </v-flex>
                        <v-flex xs12 class='mb-2'>
                            <div class='headline my-2'>Sample</div>
                            <v-card>
                                <v-card-text>0≤a,b≤100000</v-card-text>
                            </v-card>
                        </v-flex>
                    </v-layout>
                </v-tab-item>
                <v-tab-item>
                    <v-layout row wrap class='ma-1'>
                        <v-flex xs12 sm6 class='mb-2'>
                            <v-select v-model="language" :items="items" width='100'></v-select>
                        </v-flex>
                    </v-layout>
                </v-tab-item>
                <v-tab-item>
                    discussion
                </v-tab-item>
            </v-tabs-items>
        </v-flex>
    </v-layout>
</template>


<script>
    export default {
        data: function() {
            return {
                tabs: null,
                language: {
                        text: 'GNU G++17',
                        value: 'GNU G++'
                    },
                items: [{
                        text: 'GNU G++17',
                        value: 'GNU G++'
                    },
                    {
                        text: 'GNU GCC 7.3',
                        value: 'GNU GCC'
                    },
                    {
                        text: 'Clang 6.0.0',
                        value: 'Clang'
                    },
                    {
                        text: 'Python 3.6.5',
                        value: 'Python'
                    },
                    {
                        text: 'Java 10',
                        value: 'Java'
                    },
                    {
                        text: 'Go 1.10.2',
                        value: 'Go'
                    },
                    {
                        text: 'Ruby 2.5.1',
                        value: 'Ruby'
                    },
                    {
                        text: 'Rust 1.26.1',
                        value: 'Rust'
                    },
                ]
            };
        },
    }
</script>
