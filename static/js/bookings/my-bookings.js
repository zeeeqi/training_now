import "./filters.js"

let app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        bookings: [],
        loading: true,
        current_user: '',
        current_class: '',
    },
    mounted(){
        this.get_current_user()
    },
    watch: {
        current_user: {
            handler(new_user){
                this.get_user_bookings(new_user)
            }
        }
    },
    methods: {
        get_user_bookings(){
            axios.get(`/api/bookings/${this.current_user.id}/user-bookings/`)
                .then((response) => {
                    this.bookings = response.data
                    this.loading = false
                })
                .catch((error) => {
                    console.error(error)
                    this.loading = false
                })
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
        delete_booking(booking_id){
            axios.delete(`/api/bookings/${booking_id}/create-booking/`)
                .then((response) => {
                    this.get_user_bookings()
                    toastr["success"](response.data.message ,"Acción completada")
                })
                .catch((error) => {
                    console.error(error)
                    toastr["error"](error.response.data.message , "No se pudo realizar la acción")
                })
        },
        set_class(hour){
            this.current_class = hour
        },
    },
    computed: {
        have_bookings(){
            return Object.keys(this.bookings).length > 0
        }
    }

})