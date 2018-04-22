<template>
  <div>
    <apothecary-header/>
    <div id="search-block">
      <label for="search-input">Найти</label><br/>
      <input type="text" id="search-input" v-model="searchText">
    </div>
    <div id="recipes">
      <div v-for="recipe in recipes">
        <recipe-card v-bind:recipe="recipe"/>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios";

  import ApothecaryHeader from "./header/ApothecaryHeader";
  import AppInput from "./partials/AppInput";
  import RecipeCard from "./partials/RecipeCard";

  export default {
    name: "Recipes",
    components: {
      RecipeCard,
      AppInput,
      ApothecaryHeader
    },
    data() {
      return {
        searchText: "",
        recipes: []
      }
    },
    beforeMount() {
      axios.get("/api/recipes?id=" + this.searchText)
        .then(response => this.recipes = response.data)
        .catch(error => this.recipes = [])
    }
  }
</script>

<style lang="less" scoped>
  #search-block {
    margin: 10px auto;
    text-align: center;
    width: 300px;

    #search-input {
      width: 300px;
      height: 30px;
      font-size: 16px;
      border-radius: 10px;
      border: 2px solid #087e8b;
      outline: none;
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
