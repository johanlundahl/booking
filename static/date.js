

new Vue({
    el: '#app',
    created() {
        this.fetchData();
        this.interval = setInterval(function () {
            this.fetchData();
        }.bind(this), 10000);
    },
    data: {
        bookings: [],
        interval: null,
        date: '',
    },
    methods: {
        fetchData() {
            axios.get('http://localhost:5000/api/reservations?date='+this.date).then(response => {
                this.bookings = response.data;
            });
        }
    },

    beforeDestroy: function(){
        clearInterval(this.interval);
    }
});

Vue.component('return', {
    props: ['booking'],
    template: `
        <span style="color:gray;">{{ booking.return_at }}</span>
    `
});
