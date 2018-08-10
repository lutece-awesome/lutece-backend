import Vue from 'vue';

Vue.filter('nl2br', text => text.replace(/(?:\r\n|\r|\n)/g, '<br>'));
