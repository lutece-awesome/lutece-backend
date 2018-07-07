<template>
    <div class="ui pagination menu">
        <a class = 'item' v-for= "(each, index) in MenuList" :key = 'each.index' v-bind:class = '{ active : ( page == index + 1 ) }'  @click = 'each.resolve' >{{ each.index }}</a>
    </div>
</template>

<script>
    export default {
        props:{
            maxpage:{
                type: Number,
                required: true
            },
            page:{
                type: Number,
                required: true
            },
            count:{
                type: Number,
                default: 10
            },
            resolve:{
                type: Function,
                default: () =>  {}
            }
        },
        created(){
            let page = parseInt(this.page);
            let count = this.count;
            let maxpage = parseInt(this.maxpage);
            let before = count / 2;
            let after = count - 1 - before;
            let l = Math.max( 1 , page - before );
            let r = Math.min( maxpage , page + after );
            let rl = before - ( page - l );
            let rr = after - ( r - page );
            l = Math.max( 1 , l - rr );
            r = Math.min( maxpage , r + rl );
            for( let i = l ; i <= r ; ++ i){
                this.MenuList.push({
                    index: i,
                    resolve: this.resolve( i ),
                });
            }
        },
        data: function(){
            return{
                MenuList : [],
            }
        }
    }
</script>
