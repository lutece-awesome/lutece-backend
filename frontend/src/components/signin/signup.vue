
<template>
    <div class = 'ui form segment' style = 'margin:0 auto;width:600px;' >

        <h3 class = 'header' style = 'text-align:center;'> <i class = 'edit icon'></i> SIGN UP </h3>

        <div class = 'required field'>
            <label> Username </label>
            <div class="ui left icon input">
            <i class="user icon"></i>
            <input v-bind = "username" />
            </div>
        </div>

        <div class = 'required field'>
            <label> Password </label>
            <div class="ui left icon input">
                <i class="lock icon"></i>
                <input type = 'password' v-bind = "password" />
            </div>
        </div>

        <div class = 'required field' data-tooltip = "Will be used to provide gravatar in Lutece" data-position = "top left" >
            <label><i class = 'small info circle icon'></i>Email</label>
            <div class="ui left icon input">
                <i class="mail icon"></i>
                <input v-bind = "email" />
            </div>
        </div>

        <div class = 'required field'>
            <label> Display name </label>
            <div class="ui left icon input">
                <i class="cloud icon"></i>
                <input v-bind = "displayname" />
            </div>
        </div>

        <div class = 'field'>
            <label> School </label>
            <div class="ui left icon input">
                <i class="university icon"></i>
                <input v-bind = "school" />
            </div>
        </div>

        <div class = 'field'>
            <label> Company </label>
            <div class="ui left icon input">
                <i class="shopping bag icon"></i>
                <input v-bind = "company" />
            </div>
        </div>

        <div class = 'field'>
            <label> Location </label>
            <div class="ui left icon input">
                <i class="map marker icon"></i>
                <input v-bind = "location" />
            </div>
        </div>

        <div class = 'field'>
            <FormButton buttonstyle = 'ui primary fluid button' msg = 'Register' />
        </div>

    </div>
</template>

<script>
    import FormButton from '@/components/basic/formbutton.vue'
    export default {
        data: function(){
            return {
                username : '',
                password : '',
                email : '',
                displayname : '',
                school : '',
                company : '',
                location : ''
            }
        },
        components:{
            FormButton
        },
    }
</script>
