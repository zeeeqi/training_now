import "./filters.js"
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
                const day = Date.parse(new Date(booking.start).toDateString())
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
                    this.get_week_bookings()
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
                    this.get_week_bookings()
                    toastr["success"](response.data.message ,"Acción completada")
                })
                .catch((error) => {
                    console.error(error)
                    toastr["error"](error.response.data.message , "No se pudo realizar la acción")
                })
        },
        get_week_bookings(){
            this.first_day = this.first_day_of_week()
            this.last_day = this.last_day_of_week()
        
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
        first_day_of_week(){
            const first_day = new Date(this.week.getTime())
            if (first_day.getDay() == 0) {
                first_day.setDate(first_day.getDate() - 6)
            } else {
                first_day.setDate(first_day.getDate() - first_day.getDay() + 1)
            }
            return first_day
        },
        last_day_of_week(){
            const last_day = new Date(this.week.getTime())
            if (last_day.getDay() != 0) {
                last_day.setDate(last_day.getDate() + (7 - last_day.getDay()))
            }
            return last_day
        },
        set_next_week_date(){
            this.week =  new Date(new Date().setDate(new Date().getDate() + 7))
        },
        set_current_week(){
            this.week = new Date()
        },
        show_accordion(class_day){
            let class_date = new Date(class_day)
            let today = new Date()
            let next_monday = new Date()
            next_monday.setDate(today.getDate() + (7 - today.getDay()))
            if (class_date.getDate() === next_monday.getDate() + 1 || class_date.getDate() === today.getDate()){
                return true
            }

            return false
        },
    }
})
