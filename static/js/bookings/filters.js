
Vue.filter('fullDate', function (value) {
    if (value) {
        return value.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
    }
})
Vue.filter('formatDate', function (value) {
    if (value) {
        const date = new Date(value);
        return date.getHours();
    }
})
Vue.filter('toString', function (value) {
    if (value) {
        return value.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    }
})
Vue.filter('addOneHour', function (value) {
    if (value) {
        const date = new Date(value);
        date.setHours(date.getHours() + 1);
        return date
    }
})
Vue.filter('toDate', function (value) {
    if (value) {
        return new Date(value)
    }
})
Vue.filter('upperFirst', function (value) {
    if (value) {
        return value.charAt(0).toUpperCase() + value.slice(1)
    }
})
Vue.filter('toDate', function (value) {
    if (value) {
        return new Date(value)
    }
})
Vue.filter('mmddyyyy', function (value) {
    if (value) {
        return new Date(value).toLocaleDateString('es-ES', { month: '2-digit', day: '2-digit', year: 'numeric' })
    }
})