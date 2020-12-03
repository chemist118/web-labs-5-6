<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">DoTasks</a>
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <keep-alive>
            <router-link class="nav-link" to="/">Главная</router-link>
          </keep-alive>
        </li>

        <li v-if="getUser" class="nav-item">
          <keep-alive>
            <router-link class="nav-link" to="/todos">Задачи</router-link>
          </keep-alive>
        </li>
      </ul>
      <ul class="navbar-nav ml-auto">
        <li v-if="getUser" class="nav-item">
          <a class="nav-link" href="#"><i class="fas fa-user-circle"></i> {{ getUser.login }}</a>
        </li>
        <li v-if="getUser" class="nav-item">
          <a class="nav-link my-cursor" v-on:click="logout()"><i class="fas fa-sign-out-alt"></i> Выход</a>
        </li>
        <li v-if="!getUser" class="nav-item">
          <keep-alive>
            <router-link class="nav-link" to="/login"><i class="fas fa-sign-out-alt"></i> Вход</router-link>
          </keep-alive>
        </li>
        <li v-if="!getUser" class="nav-item">
          <keep-alive>
            <router-link class="nav-link" to="/registration"
              ><i class="fas fa-sign-out-alt"></i> Регистрация</router-link
            >
          </keep-alive>
        </li>
      </ul>
    </nav>
    <router-view />
    <footer class="footer navbar-fixed-bottom">
      <p class="text-center"></p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'app',
  computed: {
    getUser() {
      return this.$store.getters.user
    },
  },
  async created() {
    if (localStorage.id !== '') {
      let user = {}
      user.id = localStorage.id
      user.login = localStorage.login
      await this.$store.dispatch('SET_USER', user)
    }
  },
  methods: {
    async logout() {
      await console.log(this.getUser)
      if (this.getUser === null) {
        return
      }
      await console.log('this.getUser')
      await fetch(`/api/logout`, {
        method: 'POST',
        body: JSON.stringify({
          user_id: this.getUser.id,
        }),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      })
        .then((response) => {
          if (response.status === 200) {
            this.$store.dispatch('SET_USER', null)
            localStorage.id = ''
            localStorage.login = ''
            this.$router.push({ path: '/home' })
          } else {
            response.json().then((error) => {
              this.$store.dispatch('SET_ERROR', { type: 'login', error: error })
              this.$router.push({ path: '/login' })
            })
          }
        })
        .catch((error) => console.log(error))
    },
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0;
  margin: 0;
}

nav {
  margin-bottom: 2rem;
}

footer {
  display: flex;
  flex: 0 0 auto;
  height: 5vh;
  margin-top: 10vh;
}

.my-cursor {
  cursor: pointer;
}

.alert {
  background: linear-gradient(180deg, #5ec985 0%, #52a771 100%), #52a771 !important;
  border-radius: 8px !important;
}
.alert-danger {
  color: red !important;
  font-size: 30px !important ;
  border-color: #df2d3c !important;
}
a {
  color: #52a771 !important;
  font-weight: 600;
}
.btn-primary {
  background: linear-gradient(180deg, #5ec985 0%, #52a771 100%), #52a771 !important;
  border: none !important;
  box-shadow: 0 0 8px #52a771 !important;
}
.btn-danger {
  box-shadow: 0 0 5px red !important;
}
p {
  color: #52a771 !important;
}
h4 {
  color: white !important;
}
</style>
