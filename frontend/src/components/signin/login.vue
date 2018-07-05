<template>

    <div class="ui two column middle aligned very relaxed stackable segment grid" style = 'margin:0 auto;width:800px;'>

        <div class = 'column'>
            <div class = 'ui form' v-bind:class = '{error : iserror}' >
                <h4 style = 'text-align:center;' > <i class = 'sign in alternate icon'></i> LOG IN </h4>
                <div class = 'field'>
                    <label> Username </label>
                    <div class="ui left icon input">
                        <i class="user icon"></i>
                        <input v-model= "username" />
                    </div>
                </div>
                <div class = 'field'>
                    <label> Password </label>
                    <div class="ui left icon input">
                        <i class="lock icon"></i>
                        <input type = 'password' v-model = "password" />
                    </div>
                </div>
                <div class = 'field'>
                    <FormButton buttonstyle = 'ui primary fluid button' fluid = 'true' msg = 'Login' :action = 'login' :error = 'errorfunc' />
                </div>
                <ErrorMessage errorstyle = 'ui error message' header = 'LOGIN ERROR' v-bind:msg = errormsg  />
            </div>
        </div>

        <div class="divider-column" style = 'position: relative;padding: 0 !important;'>
            <div class="ui vertical divider"> OR </div>
        </div>

        <div class="center aligned column">
            <div style = 'vertical-align:middle;'>
                <FormButton buttonstyle = 'ui medium labeled icon positive button' icon = 'edit icon' msg = 'SIGN UP' :action = 'signup' />
            </div>
        </div>

    </div>


</template>


<script>
    import FormButton from '@/components/basic/formbutton.vue'
    import ErrorMessage from '@/components/basic/error.vue'
    import { LoginGQL } from '@/graphql/basic/login.js'
    export default {

        data: function(){
            return{
                username : '',
                password : '',
                iserror : false,
                errormsg : '',
            }
        },

        components:{
            FormButton,
            ErrorMessage
        },

        methods:{
            login: function(){
                this.iserror = false;
                return this.$apollo.mutate({
                    mutation: LoginGQL,
                    variables:{
                        username: this.username,
                        password: this.password
                    },
                }).then( response => response.data.UserLogin )
                  .then( data => {
                      if( data.state ){
                        this.redirect();
                      }else
                        throw String( data.msg )
                  })
            },
            signup: function(){
                this.$router.push( { name : 'Signup' });
            },
            redirect: function(){
                this.$router.push (this.$route.query.redirect || '/' );
            },
            errorfunc: function( error ){
                this.iserror = true;
                this.errormsg = String( error );
            }
        }
    }
</script>


