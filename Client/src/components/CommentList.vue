<template>
  <div class="card-default w-100 mx-auto">
    <h4 class="text-center">Комментарии</h4>
    <section id="section-container">
      <ul id="comments-list" class="list-group">
        <comment-item v-for="comment of comments" :comment="comment" :key="comment.id" />
      </ul>
    </section>
  </div>
</template>

<script>
import CommentItem from '@/components/CommentItem'

export default {
  name: 'CommentsList',
  props: ['comments'],
  components: {
    CommentItem,
  },
}
</script>
