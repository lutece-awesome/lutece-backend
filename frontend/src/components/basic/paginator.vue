<template>
    <div class="ui pagination menu">
        <a class = 'icon item' @click = 'firstpageresolve'  ><i class="angle double left icon"></i></a>
        <a class = 'item' v-for= "each in MenuList" :key = 'each.index' v-bind:class = '{ active : ( page == each.index ) }'  @click = 'each.resolve' >{{ each.index }}</a>
        <a class = 'icon item' @click = 'lastpageresolve' ><i class="angle double right icon"></i></a>
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
            },
        },
        created(){
            this.update();
        },
        watch:{
            page: function(){
                this.update();
            }
        },
        data: function(){
            return{
                MenuList : [],
                firstpageresolve: () => {},
                lastpageresolve: () => {}
            }
        },
        methods:{
            update: function(){
                this.MenuList.splice( 0 , this.MenuList.length );
                let page = this.page;
                let count = this.count;
                let maxpage = this.maxpage;
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
                this.firstpageresolve = this.resolve( 1 );
                this.lastpageresolve = this.resolve( maxpage );
            }
        }
    }
</script>
