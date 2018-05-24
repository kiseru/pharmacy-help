<template>
  <div>
    <apothecary-header/>
    <div class="container">
      <search-bar/>
      <div id="recipes">
        <div v-for="recipe in foundRecipes">
          <recipe-card v-bind:recipe="recipe"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios";

  import ApothecaryHeader from "./header/ApothecaryHeader";
  import RecipeCard from "./partials/RecipeCard";
  import SearchBar from "./partials/SearchBar";

  export default {
    name: "Recipes",
    components: {
      RecipeCard,
      ApothecaryHeader,
      SearchBar
    },
    data() {
      return {
        recipes: []
      }
    },
    computed: {
      foundRecipes() {
        if (this.$store.state.searchText === "") return this.recipes;
        return this.recipes.filter(recipe => recipe.id.toLowerCase().includes(this.$store.state.searchText))
      }
    },
    beforeMount() {
      axios.get("/api/recipes?id=")
        .then(response => this.recipes = response.data)
        .catch(error => this.recipes = [])
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
