console.log(location.search)     // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
  createApp({
    data() {
      return {
        id:0,
        usuario:"",
        password:"",
        email:"",
        nombre:0,
        url:'http://localhost:5000/usuarios/'+id,
       }  
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    this.id=data.id
                    this.usuario = data.usuario;
                    this.password=data.password
                    this.email=data.email
                    this.nombre=data.nombre                    
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },
        modificar() {
            let user = {
                usuario:this.usuario,
                nombre: this.nombre,
                email: this.email,
                password:this.password
            }
            var options = {
                body: JSON.stringify(user),
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            }
            let repetir = prompt("Por favor confirme el password:",);
            if (repetir==this.password) {
                fetch(this.url, options)
                    .then(function () {
                        window.location.href = "./usuarios.html";             
                    })
                    .catch(err => {
                        console.error(err);
                        alert("Error al Modificar")
                    });
            } else {
                    alert("Password incorrecto");
                    return false
            }      
        }
    },
    created() {
        this.fetchData(this.url)
    },
  }).mount('#app')
