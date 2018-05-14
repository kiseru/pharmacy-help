<template>
  <div>
    <apothecary-header v-if="user.role == 'apothecary'"/>
    <doctor-header v-else/>
    <div class="card col-md-10 align-self-center">
      <div class="card-body">
        <div class="row">
          <div class="card-title col-md-10">Сотрудники</div>
          <div class="col-md-2"><a v-bind:href="this.$route.path + '/new'"><button class="btn btn-primary">Добавить</button></a></div>
        </div>
        <div class="card-text">
          <table class="table">
            <thead class="thead-light">
              <tr>
                <th>Фамилия</th>
                <th>Имя</th>
                <th>E-mail</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="worker in workers">
                <td>{{worker.last_name}}</td>
                <td>{{worker.first_name}}</td>
                <td><a v-bind:href="'/' + user.role + '/workers/' + worker.id">{{worker.email}}</a></td>
                <td><button v-if="worker.email != user.email" class="btn btn-danger btn-sm">Удалить</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import ApothecaryHeader from "./header/ApothecaryHeader";
  import DoctorHeader from "./header/DoctorHeader"
  import axios from "axios";

  export default {
    name: "Workers",
    components: {
      ApothecaryHeader,
      DoctorHeader,
    },
    data() {
      return {
        'workers': []
      }
    },
    methods: {
      getWorkers() {
        axios.get("/api/workers")
         .then(function(response) {
           this.workers = response.data;
           console.log(this.workers);
         }.bind(this))
         .catch(error => {
           console.log(error)
         })
      }
    },
    computed: {
      user(){
        return this.$store.getters.getUser;
      }
    },
    beforeMount() {
      this.getWorkers()
    }
  }
</script>

<style lang="less" scoped>
  .card {
    margin: 20px auto;
    text-align: center;
    padding: 0;

    .card-title {
      font-size: 23px;
    }

    .card-text {
      margin-top: 10px;
    }

    .card-footer {
      padding: 10px;
    }
  }
</style>
