<template>

    <li class="list-group-item list-group-item-action comment-item">
        <span>{{comment.name}}</span>
        <span>{{ comment.email}}</span>
        <span>{{comment.body}}</span>
    </li>

</template>

<script>

    export default {
        name: "CommentItem",
        props: {
            comment: {
                type: Object,
                required: true
            }
        }
    }
</script>
