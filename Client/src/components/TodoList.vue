<template>
    <div>
        <ul id="todo-list">
            <todo-item
                v-for="todo of todos"
                :todo="todo"
                :key="todo.id"
            />
        </ul>
    </div>
</template>

<script>
    import TodoItem from '@/components/TodoItem'
    export default {
        name: "TodoList",
        props: ['todos'],
        components: {
            TodoItem
        }
    }
</script>

<style>
    ul {
        list-style: none;
        margin: 0;
        padding: 0;
    }

</style>