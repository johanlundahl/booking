
new Vue({
    el: '#app',
    created() {
        this.fetchData();
        this.interval = setInterval(function () {
            this.fetchData();
        }.bind(this), 10000);
    },
    data: {
        posts: [],
        interval: null,
    },
    methods: {
        fetchData() {
            axios.get('http://localhost:5000/api/customers').then(response => {
                this.posts = response.data;
            });
        }
    },

    beforeDestroy: function(){
        clearInterval(this.interval);
    }
});