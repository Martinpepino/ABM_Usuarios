const { createApp } = Vue
  createApp({
    data() {
      return {
        users:[],
        url:'http://localhost:5000/usuarios', 
        error:false,
        cargando:true,
        /*atributos para el guardar los valores del formulario */
        id:0,
        nombre:"", 
        password:"",
        email:"",
        nombre:"",
        protegida:"******",
    }  
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.users = data;
                    this.cargando=false
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },
        eliminar(user) {
            let confirma = confirm("Esta seguro de eliminar el usuario?");
            if (confirma == true) {
                const url = this.url+'/' + user;
                var options = {
                    method: 'DELETE',
                }
                fetch(url, options)
                    .then(res => res.text()) // or res.json()
                    .then(res => {
                        location.reload();
                    })
            } else {
                return false
            };
        },
        grabar(){
            let user = {
                usuario:this.usuario,
                nombre: this.nombre,
                email: this.email,
                password:this.password
            }
            var options = {
                body:JSON.stringify(user),
                method: 'POST',
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
                    alert("Error al Grabar")
                })   
            } else {
                alert("Password incorrecto");
                return false
            }
        },
        ver(id,password){
            alert("Password : " + password);
        }
    },
    created() {
        this.fetchData(this.url)
    },
  }).mount('#app')
