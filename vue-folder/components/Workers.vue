<template>
  <div>
    <default-header/>
    <div class="card col-md-10 align-self-center">
      <div class="card-body">
        <div class="row">
          <div class="card-title col-md-10">Сотрудники</div>
          <div class="col-md-2"><button class="btn btn-primary">Добавить</button></div>
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
              <tr>
                <td>Новикова</td>
                <td>Анна</td>
                <td>anna.novikova@mail.ru</td>
                <td><button class="btn btn-danger btn-sm">Удалить</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import DefaultHeader from "./header/DefaultHeader";

  export default {
    name: "Workers",
    components: {
      DefaultHeader
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
