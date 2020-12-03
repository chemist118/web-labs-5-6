<template>
    <form class="container w-100 mx-auto">
        <h4 class="alert alert-info text-center">Информация по задаче</h4>

        <form class="card-body">
            <b-alert class="alert alert-danger"
                     :show="dismissCountDown"
                     @dismissed="dismissCountDown=0"
                     @dismiss-count-down="countDownChanged">
                {{ getError }}
            </b-alert>

            <Loader v-if="loading"></Loader>
            <form v-else @submit.prevent="onSubmit">
                <div class="form-group">
                    <label for="title-input">Заголовок:</label>
                    <input type="text" name="title" class="form-control" id="title-input" placeholder="Заголовок"
                           v-model="title">
                </div>
                <div class="form-group">
                    <label for="description-input">Описание:</label>
                    <input type="text" name="description" class="form-control" id="description-input"
                           placeholder="Описание"
                           v-model="description">

                </div>
                <div class="form-group">
                    <label>Статус:</label>
                    <select v-model="completed" class="form-control for-margin" aria-label="Basic example">
                        <option value="true" selected>Завершенная</option>
                        <option value="false">Незавершенная</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary text-center">Обновить</button>

            </form>

        </form>

        <Loader v-if="loading"></Loader>
        <form v-else class="card-body my-comment">
            <CommentList :comments="comments"/>
        </form>

    </form>
</template>

<script>
    import Loader from '@/components/Loader.vue'
    import CommentList from '@/components/CommentList.vue'
    import CommentItem from '@/components/CommentItem.vue'

    export default {
        name: "GetTodoDescription",
        data() {
            return {
                comments: [],
                title: '',
                description: '',
                completed: false,
                id: Number(this.$route.params.id),
                loading: true,
                seen: false,
                dismissSecs: 3,
                dismissCountDown: 0
            }
        },
        components: {
            Loader,
            CommentList,
            CommentItem
        },
        computed: {
            getTodo() {
                return this.$store.getters.TODO;
            },
            todoList() {
                return this.$store.getters.TODOS;
            },
            getError() {
                return this.$store.getters.editError;
            },
            getUser() {
                return this.$store.getters.user;
            },
        },
        async created() {
            await this.$store.dispatch('SET_ERROR', {type: 'add', error: null});
            if (this.todoList.length === 0) {
                await this.$store.dispatch('FETCH_TODOS', {id: this.getUser.id });
            }
            console.log(this.todoList);
            if (this.todoList.find(t => t.id === this.id)) {
                const todo = this.todoList.find(t => t.id === this.id);
                await this.$store.dispatch('SET_TODO', todo);
                this.title = todo.title;
                this.description = todo.description;
                this.completed = todo.completed;
                await fetch(`https://jsonplaceholder.typicode.com/comments?postId=${this.id}&_limit=4`)
                    .then(response => response.json())
                    .then(json => {
                        this.comments = json;
                        this.loading = false;
                    });
                await this.$store.dispatch('SET_ERROR', {type: 'edit', error: null});
            } else {
                await this.$store.dispatch('SET_ERROR', {type: 'add', error: 'Task does not exist'});
                await this.$router.push({path: '/todos'});
            }
        },
        methods: {
            countDownChanged(dismissCountDown) {
                this.dismissCountDown = dismissCountDown
            },
            showAlert() {
                this.dismissCountDown = this.dismissSecs
            },
            async onSubmit() {
                const title = this.title === undefined ? '' : this.title.trim();
                const description = this.description === undefined ? '' : this.description.trim();

                this.loading = true;
                await fetch(`/api/todos/${this.getTodo.id}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        user_id: this.getTodo.user_id,
                        title: title,
                        description: description,
                        completed: this.completed
                    }),
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })
                    .then(response => {
                        if (response.status === 200) {
                            response.json()
                                .then(json => {
                                    this.$store.dispatch('SET_ERROR', {type: 'edit', error: null});
                                    this.$store.dispatch('EDIT_TODO', {
                                        idx: this.todoList.indexOf(this.getTodo),
                                        todo: JSON.parse(json)
                                    });

                                    this.$router.push({path: '/todos'});
                                });
                        } else {
                            response.json()
                                .then(json => {
                                    this.$store.dispatch('SET_ERROR', {type: 'edit', error: json.error});
                                    this.showAlert();
                                });
                        }
                    })
                    .catch(error => {
                        this.$store.dispatch('SET_ERROR', {type: 'edit', error: error});
                        this.showAlert();
                    });
                this.loading = false;
            }
        }
    }
</script>

<style scoped>

    label {
        float: left;
    }

    button {
        float: left;
    }

    .container {
        min-height: calc(700px - 5vh - 3rem);
        max-width: calc(100% - 40vw);
    }

    .alert {
        margin-bottom: 0;
    }

    .form-group {
        margin-bottom: 1.25rem;
    }

    .card-body {
        padding: 1.25rem 0 1.25rem 0;
    }

    .my-comment {
        margin-top: 1.5rem;
        padding: 1.25rem 0 0 0;
    }

</style>