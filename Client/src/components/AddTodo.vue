<template>
    <div class="rowcard my-rowcard card-default col-sm">

        <h4 class="alert alert-info text-left">Добавление задачи</h4>
        <form @submit.prevent="onSubmit">
			<b-alert variant="danger"
					 :show="dismissCountDown"
					 dismissible fade
					 @dismiss-count-down="countDownChanged">
				{{ textAlert }}
			</b-alert>
			<b-alert variant="success"
					 :show="dismissCountDownGood"
					 dismissible fade
					 @dismiss-count-down="countDownChangedGood">
				{{ textAlert }}
			</b-alert>

            <div class="form-group">
                <label for="title-input">Заголовок:</label>
                <input type="text" class="form-control" id="title-input" placeholder="Заголовок задачи" v-model="title">
            </div>
            <div class="form-group">
                <label for="description-input">Описание:</label>
                <input type="text" class="form-control" id="description-input" placeholder="Описание"
                       v-model="description">
            </div>
            <button type="submit" class="btn btn-primary text-center">Добавить</button>
        </form>
    </div>

</template>

<script>

    export default {
        name: "AddTodo",
        data() {
            return {
                title: '',
				textAlert: '',
                description: '',
                dismissSecs: 4,
                dismissCountDown: 0,
				dismissSecsGood: 4,
				dismissCountDownGood: 0
            }
        },
        computed: {
            getUser() {
                return this.$store.getters.user;
            },
            todoList() {
                return this.$store.getters.TODOS;
            },
            getError() {
                return this.$store.getters.addError;
            }
        },
        async created() {
            await this.$store.dispatch('SET_ERROR', {type: 'edit', error: null});
            if (this.getError !== null ){
            	console.log(this.getError);
                this.showAlert();
                await setTimeout(function () {
                    this.$store.dispatch('SET_ERROR', {type: 'add', error: null});
                }.bind(this), 5000);
            }
        },
        methods: {
            countDownChanged(dismissCountDown) {
                this.dismissCountDown = dismissCountDown
            },
			countDownChangedGood(dismissCountDownGood) {
				this.dismissCountDownGood = dismissCountDownGood;
			},
			showAlert(good) {
				if (good) {
					this.dismissCountDown = 0;
					this.dismissCountDownGood = this.dismissSecs;
					this.textAlert = 'Task successfully added';
				}
				else {
					this.dismissCountDownGood = 0;
					this.dismissCountDown = this.dismissSecs;
					this.textAlert = this.getError;
				}
			},
            async onSubmit() {
                const title = this.title === undefined ? '' : this.title.trim();
                const description = this.description === undefined ? '' : this.description.trim();

                await fetch(`/api/todos`, {
                    method: 'POST',
                    body: JSON.stringify({
                        user_id: this.getUser.id,
                        title: title,
                        description: description,
                        completed: 'false'
                    }),
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })
                    .then(response => {
                        if (response.status === 200) {
                            response.json()
                                .then(json => {
                                    this.$store.dispatch('SET_ERROR', {type: 'add', error: null});
                                    this.$store.dispatch('ADD_TODO', JSON.parse(json));
                                    this.title = '';
                                    this.description = '';
                                    this.showAlert(true)
                                });
                        } else {
                            response.json()
                                .then(json => {
                                    this.$store.dispatch('SET_ERROR', {type: 'add', error: json.error});
                                    this.showAlert(false);
                                });
                        }
                    })
                    .catch(error => {
                        this.$store.dispatch('SET_ERROR', {type:'add', error: error});
                        this.showAlert(false);
                    });
            }
        }
    }
</script>

<style>

    .my-rowcard {
        min-height: calc(700px - 5vh - 3rem);
        max-width: calc(100% - 50vw);
    }

    button {
        float: left;
    }

    label {
        float: left;
    }

</style>