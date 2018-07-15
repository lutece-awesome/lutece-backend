<template>
    <v-layout row wrap justify-center>
        <v-flex xs12 md9>
            <v-card>
                <v-card-title primary-title class='primary darken-1'>
                    <h1 class="display-1 white--text mt-2">
                        A PLUS B
                    </h1>
                </v-card-title>
                <v-tabs v-model="tabs" color="primary darken-1" dark>
                    <v-tab :ripple='false'>Description</v-tab>
                    <v-tab :ripple='false'>Editor</v-tab>
                    <v-tab :ripple='false'>Discussion</v-tab>
                </v-tabs>
                <v-card-text>
                    <v-tabs-items v-model="tabs">
                        <v-tab-item class='mt-1'>
                            <h2 class="headline primary--text mb-3">Content</h2>
                            <p>输入两个整数,输出它们的和</p>
                            <h2 class="headline primary--text mb-3">Standard Input</h2>
                            <p>输入只有一行，包含两个整数a和b.</p>
                            <h2 class="headline primary--text mb-3">Standard Output</h2>
                            <p>输出a + b</p>
                            <h2 class="headline primary--text mb-3">Constraints</h2>
                            <p>0≤a,b≤100000</p>
                        </v-tab-item>
                        <v-tab-item>
                            <v-layout row wrap>
                                <v-flex xs12 sm6>
                                    <v-select v-model="language" :items="items" width='100'></v-select>
                                </v-flex>
                            </v-layout>
                        </v-tab-item>
                        <v-tab-item>
                            discussion
                        </v-tab-item>
                    </v-tabs-items>
                </v-card-text>
            </v-card>
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
