
new Vue({
    el: '#app',
    created() {
        this.fetchData();
        this.interval = setInterval(function () {
            this.fetchData();
        }.bind(this), 10000);
    },
    data: {
        drivers: [],
        interval: null,
    },
    methods: {
        fetchData() {
            axios.get('http://localhost:5000/api/drivers').then(response => {
                this.drivers = response.data;
            });
        }
    },

    beforeDestroy: function(){
        clearInterval(this.interval);
    }
});