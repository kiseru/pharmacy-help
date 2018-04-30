<template>
  <div>
    <apothecary-header/>
    <div class="container">
      <search-bar v-bind:search-obj="searchObj"/>
      <div id="recipes">
        <div v-for="recipe in recipes">
          <recipe-card v-bind:recipe="recipe"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios";

  import ApothecaryHeader from "./header/ApothecaryHeader";
  import AppInput from "./partials/AppInput";
  import RecipeCard from "./partials/RecipeCard";
  import SearchBar from "./partials/SearchBar";

  export default {
    name: "Recipes",
    components: {
      RecipeCard,
      AppInput,
      ApothecaryHeader,
      SearchBar
    },
    data() {
      return {
        searchObj: {
          text: ""
        },
        recipes: [
          {
            id: 1,
            patientName: "asdfasdf",
            doctorName: "asdfasdf",
            date: "24.02.1994"
          },
          {
            id: 1,
            patientName: "asdfasdf",
            doctorName: "asdfasdf",
            date: "24.02.1994"
          },
          {
            id: 1,
            patientName: "asdfasdf",
            doctorName: "asdfasdf",
            date: "24.02.1994"
          }
        ]
      }
    },
    beforeMount() {
      // axios.get("/api/recipes?id=" + this.searchText)
      //   .then(response => this.recipes = response.data)
      //   .catch(error => this.recipes = [])
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
