<template>
    <div class="container">
        <div class="row">
            <AddTodo/>
            <FiltersTodo/>
        </div>
    </div>
</template>

<script>
    import AddTodo from '@/components/AddTodo.vue'
    import FiltersTodo from "../FiltersTodo";

    export default {
        name: 'Todos',
        components: {
            FiltersTodo,
            AddTodo
        }
    }
</script>

<style scoped>

    .container {
        max-width: calc(100% - 10vw);
    }

</style>