
Vue.component('post-count', {
    data: function(){
        return {
            count: 1
        }
    },
    created() {
        axios.get('http://localhost:5000/api/drivers').then(response => {
            this.count = response.data.length;
        });
    },
    template: `
        <div>Drivers ({{count}})</div>
    `
});

new Vue({ el: '#post-count' });

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
            axios.get('http://localhost:5000/api/drivers').then(response => {
                this.posts = response.data;
            });
        }
    },

    beforeDestroy: function(){
        clearInterval(this.interval);
    }
});