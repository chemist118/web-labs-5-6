import Vue from 'vue'
import Vuex from "vuex";

Vue.use(Vuex);

const store = new Vuex.Store({
	// Состояние приложения
    state: {
        user: null,
		// Тудушки
        todos: [],
        todo: {},
		// Текущие ошибки
        loginError: null,
        registrationError: null,
        addError: null,
        editError: null,
        notFoundError: null
    },
	
	getters: {
        user: state => {
            return state.user;
        },
        TODOS: state => {
            return state.todos;
        },
        COMPL_TODOS: state => {
            return state.todos.filter(t => t.completed === 'true');
        },
        NOT_COMPL_TODOS: state => {
            return state.todos.filter(t => t.completed === 'false');
        },
        SEARCH_TODOS: state => (title) => {
            return state.todos.filter(t => t.title.indexOf(title) > -1);
        },
        TODO: state => {
            return state.todo;
        },
        loginError: state => {
            return state.loginError;
        },
        registrationError: state => {
            return state.registrationError;
        },
        addError: state => {
            return state.addError;
        },
        editError: state => {
            return state.editError;
        },
        notFoundError: state => {
            return state.notFoundError;
        }
    },

    mutations: {
        SET_USER: (state, payload) => {
            state.user = payload;
        },

        SET_TODOS: (state, payload) => {
            state.todos = payload;
        },

        SET_TODO: (state, payload) => {
            state.todo = payload;
        },

        SET_ERROR: (state, {type, error}) => {
            switch (type) {
                case 'login': {
                    state.loginError = error;
                    break;
                }
                case 'registration': {
                    state.registrationError = error;
                    break;
                }
                case 'add': {
                    state.addError = error;
                    break;
                }
                case 'edit': {
                    state.editError = error;
                    break;
                }
                case 'notFound': {
                    state.notFoundError = error;
                    break;
                }
            }
        },

        ADD_TODO: (state, payload) => {
            state.todos.push(payload);
        },

        EDIT_TODO: (state, {idx, todo}) => {
            state.todos.splice(idx, 1, todo);
        },

        DELETE_TODO: (state, payload) => {
            state.todos.splice(payload, 1);
        },
    },

    actions: {
		// Действие получения всех тудушек
		FETCH_TODOS: ({commit}, payload) => {

            return fetch(`/api/todos?user_id=${payload.id}`, {
                method: 'GET'
            })
                .then(response => {
                    if (response.status === 200) {
                        return response.json()
                            .then(json => {
                                commit('SET_TODOS', JSON.parse(json));
                            });
                    } else if (response.status === 300) {
                        return response.json()
                            .then(json => {
                                commit('ADD_TODO', JSON.parse(json));
                            });
                    }
                })
                .catch(error => console.log(error));
        },

        SET_USER: async ({commit}, payload) => {
            commit('SET_USER', payload);
        },

        SET_ERROR: ({commit}, payload) => {
            commit('SET_ERROR', payload);
        },

        SET_TODO: async ({commit}, payload) => {
            commit('SET_TODO', payload);
        },

        ADD_TODO: async ({commit}, payload) => {
            commit('ADD_TODO', payload);
        },

        EDIT_TODO: async ({commit}, payload) => {

            commit('EDIT_TODO', payload);
        },

        DELETE_TODO: async ({commit}, payload) => {
            commit('DELETE_TODO', payload);
        }

    },
});
export default store;