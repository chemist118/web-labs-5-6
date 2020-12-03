<template>
    <div class="container">
        <section class="card card-default w-50 mx-auto">
            <h4 class="card-header alert-info text-center">Login</h4>

            <form class="card-body" @submit.prevent="onSubmit">
                <b-alert variant="danger"
                         :show="dismissCountDown"
						 dismissible fade
                         @dismiss-count-down="countDownChanged">
                    {{ getError }}
                </b-alert>

                <div class="form-group">
                    <label for="login-input">Username:</label>
                    <input type="text" name="login" class="form-control" id="login-input" placeholder="Username"
                           v-model="login">
                </div>
                <div class="form-group">
                    <label for="password-input">Password:</label>
                    <input type="password" name="password" class="form-control" id="password-input" placeholder="******"
                           v-model="password">
                </div>
                <button type="submit" class="btn btn-primary text-center">Login to account</button>
            </form>
        </section>
    </div>
</template>


<script>

    export default {
        name: 'Login',
        data() {
            return {
                login: '',
                password: '',
                dismissSecs: 4,
                dismissCountDown: 0
            }
        },
        computed: {
            getUser() {
                return this.$store.getters.user;
            },
            getError() {
                return this.$store.getters.loginError;
            }
        },
        async created() {
            if (this.getError !== null ) {
                this.showAlert();
                await setTimeout(function () {
                    this.$store.dispatch('SET_ERROR', {type: 'login', error: null});
                }.bind(this), 5000);
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
                let login = this.login === undefined ? '' : this.login.trim();
                let password = this.password === undefined ? '' : this.password.trim();

                await fetch(`/api/login?user_login=${login}&user_password=${password}`, {
                    method: 'GET'
                })
                    .then(response => {
                        if (response.status === 200) {
                            response.json()
                                .then(json => {
                                    this.$store.dispatch('SET_ERROR', {type: 'login', error: null});
                                    this.$store.dispatch('SET_USER', JSON.parse(json));
                                    localStorage.id = this.getUser.id;
                                    localStorage.login = this.getUser.login;
                                    this.$router.push({path: '/home'});
                                });
                        } else {
                            response.json()
                                .then(json => {
                                    this.$store.dispatch('SET_ERROR', {type: 'login', error: json.error});
                                    this.showAlert();
                                });
                        }
                    })
                    .catch(error => {
                        this.$store.dispatch('SET_ERROR', {type: 'login', error: error});
                        this.showAlert();
                    });
            }
        }
    }
</script>

<style>

    label {
        float: left;
    }

    .container {
        min-height: calc(700px - 5vh - 3rem);
        height: calc(100% - 12.5rem - 5vh);
        max-width: calc(100% - 40vw);
    }

</style>