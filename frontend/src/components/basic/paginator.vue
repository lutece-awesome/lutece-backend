<template>
    <div class="ui pagination menu">
        <router-link class = 'item' v-for= "each in MenuList" :key = 'each.index' to = each.url >{{ each.index }}</router-link>
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
            resolve_url:{
                type: Function,
                default: () => {}
            }
        },
        created(){
            let page = parseInt(this.page);
            let count = this.count;
            let maxpage = parseInt(this.maxpage);
            page = Math.max( maxpage , 1 );
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
                    url: this.resolve_url( i ),
                });
            }
        },
        data: function(){
            return{
                MenuList : []
            }
        }
    }
</script>
