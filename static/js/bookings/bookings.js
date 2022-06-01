

let app = new Vue({
    el: '#app',
    delimiters: ['[[',']]'],
    data:{
        available_bookings: {},
        current_class: '',
        current_user: '',
        week: new Date(),
        first_day: '',
        last_day: '',
    },
    mounted() {
        this.get_current_user()
    },
    watch:{
        week: {
            handler(new_week){
                this.get_week_bookings(new_week)
            },
            immediate: true
        }
    },
    methods: {
        have_bookings(){
            
            return Object.keys(this.available_bookings).length
        },
        get_current_user() {
            axios.get('/api/users/current-user')
                .then(response => {
                    this.current_user = response.data
                })
                .catch(error => {
                    console.error(error)
                })
        },
        group_by_day(bookings) {
            const grouped = {}
            bookings.forEach((booking)=>{
                const day = Date.parse(new Date(booking.start.slice(0,-1)).toDateString())
                if(!grouped[day]){
                    grouped[day] = []
                }
                grouped[day].push(booking)
            })
            return grouped
        },
        create_booking(booking_id){
            axios.post(`/api/bookings/${booking_id}/create-booking/`)
                .then((response) => {
                    this.get_week_bookings(new Date('2022-06-06'))
                    toastr["success"](response.data.message ,"Acción completada")
                })
                .catch((error) => {
                    console.error(error)
                    toastr["error"](error.response.data.message , "No se pudo realizar la acción")
                })
        },
        delete_booking(booking_id){
            axios.delete(`/api/bookings/${booking_id}/create-booking/`)
                .then((response) => {
                    this.get_week_bookings(new Date('2022-06-06'))
                    toastr["success"](response.data.message ,"Acción completada")
                })
                .catch((error) => {
                    console.error(error)
                    toastr["error"](error.response.data.message , "No se pudo realizar la acción")
                })
        },
        get_week_bookings(){
            this.first_day = this.first_day_of_week(this.week)
            this.last_day = this.last_day_of_week(this.week)
        
            const params = {
                start_date: `${this.first_day.getFullYear()}-${this.first_day.getMonth()+1}-${this.first_day.getDate()}`,
                end_date: `${this.last_day.getFullYear()}-${this.last_day.getMonth()+1}-${this.last_day.getDate()}`
            }
            axios.get('/api/bookings/get-bookings/', { params }).
                then((response) => {
                    this.available_bookings = this.group_by_day(response.data)
                })
        },
        set_class(hour){
            this.current_class = hour
        },
        user_in_class(users){
            return users.find(user => user.id == this.current_user.id)
        },
        first_day_of_week(date){
            const first_day = new Date(date.getTime())
            first_day.setDate(first_day.getDate() - first_day.getDay() + 1)
            return first_day
        },
        last_day_of_week(date){
            const last_day = new Date(date.getTime())
            last_day.setDate(last_day.getDate() + (7 - last_day.getDay()))
            return last_day
        },
        set_next_week_date(){
            this.week =  new Date(new Date().setDate(new Date().getDate() + 7))
        },
        set_current_week(){
            this.week = new Date()
        }
    },
    filters: {
        fullDate: function(value) {
            if (value) {
                return new Date(value).toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
            }
        },
        formatDate: function(value) {
            if (value) {
                const date = new Date(value);
                return date.getHours();
            }
        },
        toString: function(value){
            if (value) {
                return value.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
            }
        },
        addOneHour: function(value){
            if (value) {
                const date = new Date(value);
                date.setHours(date.getHours() + 1);
                return date
            }
        },
        toDate: function(value){
            if (value) {
                return new Date(value)
            }
        },
        upperFirst: function(value){
            if (value) {
                return value.charAt(0).toUpperCase() + value.slice(1)
            }
        },
        slicedDate: function(value){
            if (value) {
                return new Date(value.slice(0,-1))
            }
        },
        mmddyyyy: function(value){
            if (value) {
                return new Date(value).toLocaleDateString('es-ES', { month: '2-digit', day: '2-digit', year: 'numeric' })
            }
        }
    }
})
