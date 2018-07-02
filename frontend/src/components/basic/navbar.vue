<!--
    Navigation Bar
-->
<template>
    <div class = 'ui fixed top borderless large menu'>
        <div class = 'ui container'>
            <div class="header item">Lutece</div>
            <router-link to="/home" class = 'item' active-class = 'active'  >Home</router-link>
        </div>
    </div>
</template>

<script>
    export default {
        data: function(){
            return {
                
            }
        }
    }
</script>