<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <span class="navbar-brand">Pharmacy Help</span>
    </nav>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-4 align-self-center form-group">
          <label for="search-input">Найти</label><br/>
          <input type="text" id="search-input" class="form-control" v-model="searchText">
        </div>
      </div>
      <div id="recipes">
        <div v-for="recipe in recipes">
          <recipe-card v-bind:recipe="recipe"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import RecipeCard from "./partials/RecipeCard";

  export default {
    name: "PatientRecipes",
    components: {
      RecipeCard
    },
    data() {
      return {
        searchText: "",
        recipes: [
          {
            id: "asdfadfa",
            patientName: "asdfasdfas",
            doctorName: "adadf",
            date: "24.02.2991"
          },
          {
            id: "asdfadfa",
            patientName: "asdfasdfas",
            doctorName: "adadf",
            date: "24.02.2991"
          }
        ]
      }
    }
  }
</script>

<style lang="less" scoped>
  .container {
    margin-top: 20px;

    .form-group {
      text-align: center;
    }
  }

  #recipes {
    display: grid;
    margin: 10px auto;
  }

  @media screen and (min-width: 1080px) {
    #recipes {
      grid-template-columns: 540px 540px;
      width: 1080px;
    }
  }

  @media screen and (max-width: 1079px) {
    #recipes {
      grid-template-columns: 540px;
      width: 540px;
    }
  }
</style>
