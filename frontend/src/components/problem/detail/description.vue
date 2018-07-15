<template>
    <v-card-text>
        <h2 class="headline primary--text mb-3">Content</h2>
        <div> {{ content }} </div>
        <h2 class="headline primary--text mb-3">Standard Input</h2>
        <div> {{ standardInput }} </div>
        <h2 class="headline primary--text mb-3">Standard Output</h2>
        <div> {{ standardOutput }} </div>
        <h2 class="headline primary--text mb-3">Constraints</h2>
        <div> {{ constraints }} </div>
    </v-card-text>
</template>


<script>
    export default {
        props: ['content' , 'standardInput' , 'standardOutput' , 'constraints' , 'resource' , 'note' ],
        data: function() {
            return {
            };
        },
    }
</script>
