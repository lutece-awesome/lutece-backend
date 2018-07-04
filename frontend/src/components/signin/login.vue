<template>

    <div class="ui two column middle aligned very relaxed stackable segment grid" style = 'margin:0 auto;width:800px;'>

        <div class = 'column'>
            <div class = 'ui form'>
                <h4 style = 'text-align:center;' > <i class = 'sign in alternate icon'></i> LOG IN </h4>
                <div class = 'field'>
                    <label> Username </label>
                    <div class="ui left icon input">
                        <i class="user icon"></i>
                        <input v-bind = "username" />
                    </div>
                </div>
                <div class = 'field'>
                    <label> Password </label>
                    <div class="ui left icon input">
                        <i class="lock icon"></i>
                        <input type = 'password' v-bind = "password" />
                    </div>
                </div>
                <div class = 'field'>
                    <FormButton buttonstyle = 'ui primary fluid button' fluid = 'true' msg = 'Login' :action = 'login' :error = 'loginerror' />
                </div>
            </div>
        </div>

        <div class="divider-column" style = 'position: relative;padding: 0 !important;'>
            <div class="ui vertical divider"> OR </div>
        </div>

        <div class="center aligned column">
            <div style = 'vertical-align:middle;'>
                <FormButton buttonstyle = 'ui medium labeled icon positive button' icon = 'edit icon' msg = 'SIGN UP' />
            </div>
        </div>

    </div>
</template>


<script>
    import FormButton from '@/components/basic/formbutton.vue'

    export default {
        data: function(){
            return{
                username : '',
                password : '',
            }
        },
        components:{
            FormButton
        },

        methods:{
            login: function(){
                
            },
            loginerror: function( error ){
                alert( error );
            },
            signup: function(){
                
            }
        }
    }
</script>

<style scoped>

</style>

