<template>
  <div>
    <apothecary-header/>
    <div id="search-input">
      <app-input id="search" label="Найти"/>
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
        recipes: [
          {
            id: "906635418151ba60480cd745256310229175",
            patientName: "asdfas",
            doctorName: "asdfasdf",
            date: "28.07.2018"
          },
          {
            id: "906635418151ba60480cd745256310229175",
            patientName: "asdfas",
            doctorName: "asdfasdf",
            date: "28.07.2018"
          }
        ]
      }
    },
    /*beforeMount() {
      axios.get("/api/recipes")
        .then(response => this.recipes = response.data)
        .catch(error => this.recipes = [])
    }*/
  }
</script>

<style lang="less" scoped>
  #search-input {
    margin: 10px auto;
    text-align: center;
    width: 300px;
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
