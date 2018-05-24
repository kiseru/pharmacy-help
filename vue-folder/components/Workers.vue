<template>
  <div>
    <default-header/>
    <div class="card col-md-10 align-self-center">
      <div class="card-body">
        <div class="row">
          <div class="card-title col-md-10">Сотрудники</div>
          <div class="col-md-2"><a class="btn btn-primary" href="/workers/new">Добавить</a></div>
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
                <td>{{ worker.first_name }}</td>
                <td>{{ worker.last_name }}</td>
                <td>{{ worker.email }}</td>
                <td>
                  <button class="material-icons bg-danger border-0 rounded text-light p-1 mx-1">
                    delete_forever
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  import DefaultHeader from "./header/DefaultHeader";

  export default {
    name: "Workers",
    components: {
      DefaultHeader
    },
    data() {
      return {
        workers: []
      };
    },
    beforeMount() {
      axios.get("/api/workers?query=")
        .then(response => this.workers = response.data);
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
