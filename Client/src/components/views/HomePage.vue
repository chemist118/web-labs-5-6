<template>
    <div class="container">
        <div v-if="getUser" class="alert alert-info text-center">
			Вы авторизованы
        </div>
        <div v-else class="alert alert-info text-center">
			Вы не авторизованы
        </div>
    </div>
</template>


<script>
	export default {
        name: 'Home',
        computed: {
            getUser() {
                 return this.$store.getters.user;
            }
        }
    }
</script>

<style>
    .container {
        min-height: calc(700px - 5vh - 3rem);
        height: calc(100% - 12.5rem - 5vh);
        max-width: calc(100% - 40vw);
    }
</style>