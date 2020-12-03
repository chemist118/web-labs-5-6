<template>
    <div class="rowcard my-rowcard card-default mx-auto col-sm">
        <b-alert show variant="danger">
            {{ getError }}
        </b-alert>
    </div>
</template>

<script>
    export default {
        name: "NotFound",
        computed: {
            getError() {
                return this.$store.getters.notFoundError;
            }
        },
		created() {
            this.$store.dispatch('SET_ERROR', {type: 'notFound', error: 'Not Found'});
        }
    }
</script>