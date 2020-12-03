<template>
    <div class="container">
        <section class="card card-default w-50 mx-auto">
            <h4 class="card-header alert-info text-center">Registration</h4>
            <form class="card-body" @submit.prevent="onSubmit">
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
                    <label for="login-input">Username:</label>
                    <input type="text" name="login" class="form-control" id="login-input" placeholder="Username"
                           v-model="login">
                </div>
                <div class="form-group">
                    <label for="password-input">Password:</label>
                    <input type="password" name="password" class="form-control" id="password-input"
                           placeholder="******" v-model="password1">
                </div>
                <div class="form-group">
                    <label for="password2-input">Password confirmation:</label>
                    <input type="password" name="password2" class="form-control" id="password2-input"
                           placeholder="******" v-model="password2">
                </div>
                <button type="submit" class="btn btn-primary">Register</button>
            </form>
        </section>
    </div>
</template>


<script>
    export default {
        name: 'Registration',
        data() {
            return {
                login: '',
				textAlert: '',
                password1: '',
                password2: '',
                dismissSecs: 4,
                dismissCountDown: 0,
				dismissCountDownGood: 0
            }
        },
        computed: {
            getError() {
                return this.$store.getters.registrationError;
            }
        },
        async created() {
            if (this.getError !== null) {
                await this.$store.dispatch('SET_ERROR', {type: 'registration', error: null});
            }
        },
        methods: {
            countDownChanged(dismissCountDown) {
                this.dismissCountDown = dismissCountDown;
            },
			countDownChangedGood(dismissCountDownGood) {
				this.dismissCountDownGood = dismissCountDownGood;
			},
            showAlert(good) {
            	if (good) {
					this.dismissCountDown = 0;
					this.dismissCountDownGood = this.dismissSecs;
					this.textAlert = 'You are successfully registered';
				}
				else {
					this.dismissCountDownGood = 0;
					this.dismissCountDown = this.dismissSecs;
					this.textAlert = this.getError;
				}
            },
            async onSubmit() {
                let login = this.login === undefined ? '' : this.login.trim();
                let password1 = this.password1 === undefined ? '' : this.password1.trim();
                let password2 = this.password2 === undefined ? '' : this.password2.trim();

                await fetch(`http://localhost:5000/registration`, {
                    method: 'POST',
                    body: JSON.stringify({
                        login: login,
                        password1: password1,
                        password2: password2
                    }),
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })
                    .then(response => {
                        if (response.status === 200) {
                            response.json()
                                .then(json => {
									this.showAlert(true);
                                });
                        } else {
                            response.json()
                                .then(json => {
                                    this.$store.dispatch('SET_ERROR', {type: 'registration', error: json.error});
                                    this.showAlert(false);
                                });
                        }
                    })
                    .catch(error => {
                        this.$store.dispatch('SET_ERROR', {type: 'registration', error: error});
                        this.showAlert(false);
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