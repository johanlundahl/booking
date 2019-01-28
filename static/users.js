new Vue({
    el: '#app',
    created() {
        this.fetchData();
        this.interval = setInterval(function () {
            this.fetchData();
        }.bind(this), 10000);
    },
    data: {
        users: [],
        interval: null,
    },
    methods: {
        fetchData() {
            axios.get('http://localhost:5000/api/users').then(response => {
                this.users = response.data;
            });
        }
    },

    beforeDestroy: function(){
        clearInterval(this.interval);
    }
});

new Vue({
  el: '#add-form',
  data: {
    name: '',
    email: ''
  },
  methods: {
    processForm: function() {
        console.log({ name: this.name, email: this.email });
        axios.post('/api/users', { "name": this.name, "email": this.email, "password": "12345"})
        .then(response => {})
        .catch(e => {
            console.log(e)
        });
    }
  }
});