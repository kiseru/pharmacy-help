<template>
  <div>
    <patient-header/>
    <div class="container">
      <search-bar  v-bind:search-obj="searchObj"/>
      <div id="recipes">
        <div v-for="recipe in recipes">
          <recipe-card v-bind:recipe="recipe"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import PatientHeader from "./header/PatientHeader";
  import RecipeCard from "./partials/RecipeCard";
  import SearchBar from "./partials/SearchBar";

  export default {
    name: "PatientRecipes",
    components: {
      PatientHeader,
      RecipeCard,
      SearchBar
    },
    data() {
      return {
        searchObj: {
          text: ""
        },
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
